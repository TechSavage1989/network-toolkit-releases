"""One-time guarded v1.17.63 binary-only asset revision; no source or tag changes."""
import hashlib,json,os,pathlib,re,subprocess,sys,zipfile,stat,struct
R='TechSavage1989/network-toolkit-releases'; TAG='v1.17.63'; BRANCH='binary-revision-v1.17.63'
OLD='7fc0947d006831f1364cd0e25f14306bac0768ac'; RID=423040841
EXPECTED={'Network_Toolkit_1.17.63_Update.zip':(673573020,'ee45bbd76a3663982d177925e171d0a2fcb086b6fd7e2618995f3533ced7d1a2'),'SHA256SUMS':(673573019,'fa9f7ace2aa473cea186509f669ff3e0db2c041316693fc053cc40d016685d24')}
REQUEST='.release-revision-1.17.63.json'; FOLDER=pathlib.Path('binaries/1.17.63'); BACKUP=pathlib.Path('previous-release')
def require(x,msg):
 if not x:raise RuntimeError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def gh(path):return json.loads(subprocess.check_output(['gh','api',path]))
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def request():
 q=json.loads(pathlib.Path(REQUEST).read_text());require(set(q)=={'payload_commit','source_commit','zip_sha256','exe_sha256'},'Unexpected request fields')
 for k,v in q.items():require(re.fullmatch('[0-9a-f]{40}' if k.endswith('commit') else '[0-9a-f]{64}',v),'Invalid request hash')
 require(os.environ['GITHUB_REPOSITORY']==R and os.environ['GITHUB_REF']=='refs/heads/'+BRANCH,'Wrong repository or trigger branch')
 head=git('rev-parse','HEAD');require(head==os.environ['GITHUB_SHA'],'Wrong checkout')
 require(git('rev-parse','HEAD^')==q['payload_commit'],'Request must directly follow selected payload')
 require(git('diff','--name-only','HEAD^','HEAD')==REQUEST,'Request commit must change only request file')
 require(gh(f'repos/{R}/git/ref/heads/{BRANCH}')['object']['sha']==head,'Request branch changed')
 require(gh(f'repos/{R}/git/ref/heads/main')['object']['sha']==q['payload_commit'],'Main payload changed')
 source=gh('repos/TechSavage1989/network-toolkit/git/ref/tags/'+TAG)
 require(source['object']['type']=='commit' and source['object']['sha']==q['source_commit'],'Main source tag changed')
 source_release=gh('repos/TechSavage1989/network-toolkit/releases/tags/'+TAG)
 require(not source_release['draft'] and not source_release['prerelease'],'Source release is not stable')
 assets={a['name']:a for a in source_release['assets']}
 require(assets['Network_Toolkit.exe']['digest']=='sha256:'+q['exe_sha256'],'Source EXE digest differs')
 require(assets['Network_Toolkit_1.17.63_Update.zip']['digest']=='sha256:'+q['zip_sha256'],'Source ZIP digest differs')
 return q

def validate(q):
 name='Network_Toolkit_1.17.63_Update.zip';data=(FOLDER/name).read_bytes();require(sha(data)==q['zip_sha256'],'ZIP digest differs')
 require((FOLDER/'SHA256SUMS').read_text()==q['zip_sha256']+'  '+name+'\n','External checksums differ')
 prefix='Network_Toolkit_1.17.63/';exe='Network_Toolkit_1.17.63_Windows_x64.exe'
 allowed={prefix+n for n in [exe,'UPDATING.txt','THIRD_PARTY_NOTICES.txt','SHA256SUMS']}
 with zipfile.ZipFile(FOLDER/name) as z:
  require(len(z.infolist())==4 and set(z.namelist())==allowed,'ZIP must contain exactly four allowed files')
  for i in z.infolist():require(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'Invalid ZIP member')
  b=z.read(prefix+exe);require(sha(b)==q['exe_sha256'] and b[:2]==b'MZ','EXE differs')
  pe=struct.unpack_from('<I',b,0x3c)[0];require(b[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',b,pe+4)[0]==0x8664,'Not Windows x64 PE')
  idx=b.find(bytes.fromhex('bd04effe00000100'));require(idx>=0,'Missing version resource')
  v=struct.unpack_from('<6I',b,idx);require(v[2:6]==(65553,4128768,65553,4128768),'Wrong PE version')
  lines=z.read(prefix+'SHA256SUMS').decode().splitlines();sums={}
  for line in lines:
   h,n=line.split('  ',1);require(n not in sums,'Duplicate checksum');sums[n]=h
  require(set(sums)=={exe,'UPDATING.txt','THIRD_PARTY_NOTICES.txt'},'Internal checksum allowlist differs')
  for n,h in sums.items():require(sha(z.read(prefix+n))==h,'Internal checksum differs')

def snapshot():
 ref=gh(f'repos/{R}/git/ref/tags/{TAG}');require(ref['object']['type']=='commit' and ref['object']['sha']==OLD,'Old tag changed')
 release=gh(f'repos/{R}/releases/tags/{TAG}');require(release['id']==RID and not release['draft'] and not release['prerelease'],'Release identity/status differs')
 assets=release['assets'];require(len(assets)==2 and {a['name'] for a in assets}==set(EXPECTED),'Unexpected asset inventory')
 for a in assets:
  ident,h=EXPECTED[a['name']];require(a['id']==ident and a['digest']=='sha256:'+h and a['state']=='uploaded','Original asset changed')
 return {'release_id':release['id'],'tag':ref['object'],'assets':sorted([{'id':a['id'],'name':a['name'],'size':a['size'],'digest':a['digest']} for a in assets],key=lambda a:a['name'])}

def verify_backup(before):
 for a in before['assets']:
  b=(BACKUP/a['name']).read_bytes();require(len(b)==a['size'] and 'sha256:'+sha(b)==a['digest'],'Backup differs')

def main():
 require(len(sys.argv)==2 and sys.argv[1] in ['backup','publish'],'Expected backup or publish')
 q=request();validate(q);before=snapshot()
 if sys.argv[1]=='backup':
  require(not BACKUP.exists(),'Backup directory already exists');BACKUP.mkdir()
  subprocess.run(['gh','release','download',TAG,'--repo',R,'--dir',str(BACKUP)],check=True)
  verify_backup(before);require(snapshot()==before,'Release changed during backup')
  (BACKUP/'release-before.json').write_text(json.dumps(before,indent=2)+'\n');return
 require(json.loads((BACKUP/'release-before.json').read_text())==before,'Backup metadata differs');verify_backup(before)
 request();require(snapshot()==before,'Release changed before replacement')
 # Checksums last: partial replacement cannot pass updater SHA-256 validation.
 for name in ['Network_Toolkit_1.17.63_Update.zip','SHA256SUMS']:
  subprocess.run(['gh','release','upload',TAG,str(FOLDER/name),'--repo',R,'--clobber'],check=True)
 item=gh(f'repos/{R}/releases/tags/{TAG}');require(item['id']==RID and len(item['assets'])==2 and {a['name'] for a in item['assets']}==set(EXPECTED),'Revised inventory differs')
 for a in item['assets']:require(a['digest']=='sha256:'+sha((FOLDER/a['name']).read_bytes()),'Revised digest differs')
 require(gh(f'repos/{R}/git/ref/tags/{TAG}')['object']==before['tag'],'Old tag unexpectedly changed')
 print('Verified binary-only v1.17.63 revision; release ID and tag preserved.')
if __name__=='__main__':main()
