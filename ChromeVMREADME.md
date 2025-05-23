Google Chrome VM README.md

0. Create VM
 
1. Gen SSH key and add to GitHub.

```
 ssh-keygen -t ed25519 -C "youremail@here.com"
```
- Make sure the email is the one associated with your GitHub account
- Do not save to a custom file, just enter through
- To find the key:
```
cd .ssh
```
- Vim or Nano into the file with the .pub extension, and copy the entire key (incluidng the ssh-ed25519 and your email)

2. To add to GitHub, go to Settings > Add SSH key.
    - First, go to the folder in the VM where you saved the ssh key. Nano into the one with the .pub suffix
    - Copy the entirety of the key and paste it into GitHub

3. Install Python3, venv, and virtual displayer.

```
 sudo apt-get update
 sudo apt-get install python3
 sudo apt-get install python3.11-venv
 sudo apt-get instlal -y xvfb
 python3 -m venv scraper_env
 source scraper_env/bin/activate
```

4. Clone the repository.

```
 git clone git@github.com:wu-msds-capstones/msds-capstone-repo-aryan-tyler.git
 cd msds-capstone-repo-aryan-tyler/scrapers
```
5. Install the required packages.

```
 pip install -r 'requirements.txt'
```

6. Install the Chrome Driver

### Download and Install Chrome

```
sudo apt-get update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```
If you don't have wget, install it with

```
sudo apt install wget
```
Once you have gotten the .deb file, install from it using
```
sudo dpkg -i google-chrome-stable_current_amd64.deb
```


### Install all Dependencies

```
sudo apt-get install -f
```

### Install Chrome

```
wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip
```
