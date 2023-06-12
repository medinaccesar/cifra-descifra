import os
import subprocess
locale_dir = 'locale'

def compile_po_files():
    for root, dirs, files in os.walk(locale_dir):        
        for file in files:
            if file.endswith('.po') and root is not locale_dir:
                po_file = os.path.join(root, file)
                #lang = os.path.splitext(po_file)[1][1:]
                print('Se compila',root)
                mo_file = po_file.replace('.po', '.mo')
                msgfmt_cmd = f'msgfmt {po_file} -o {mo_file}'
                subprocess.call(msgfmt_cmd, shell=True)   

if __name__ == "__main__":
   
    compile_po_files()