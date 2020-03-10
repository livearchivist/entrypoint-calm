export PS1="\[\033[36m\]\u\[\033[m\]:\[\033[33;1m\]\w\[\033[m\]\$ "
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad
export GOPATH=$HOME/golang
export GOROOT=/usr/local/opt/go/libexec
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin
export DVMIP=10.4.100.128
HISTFILESIZE=1000000000
HISTSIZE=1000000

alias k=kubectl
alias kips='kubectl describe nodes | grep InternalIP'
alias imlb='kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.7.3/manifests/metallb.yaml'
alias des='echo export KUBECONFIG=$(ls *kubectl.cfg) > .envrc; direnv allow'
alias hs='helm init --client-only; helm tiller start'
alias sbftp='sftp -oUser=psb33655 psb33655.seedbox.io'
alias uvpn="launchctl unload /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*"
alias lvpn="launchctl load /Library/LaunchAgents/com.paloaltonetworks.gp.pangp*"
alias udrv="launchctl unload /Library/LaunchAgents/inSync*"
alias ldrv="launchctl load /Library/LaunchAgents/inSync*"
alias usen="sudo launchctl unload /Library/LaunchDaemons/com.sentinelone.sentineld*; launchctl unload /Library/LaunchAgents/com.sentinelone.agent.plist"
alias lsen="sudo launchctl load /Library/LaunchDaemons/com.sentinelone.sentineld*; launchctl load /Library/LaunchAgents/com.sentinelone.agent.plist"
alias uwlk="sudo /usr/bin/profiles -R -p walkme.extensionpid"
alias eptb="tar -zcvf entrypoint.tar.gz entrypoint"
alias ls='ls -GFh'
alias ll='ls -l'
alias di='ssh mhaigh@diamond.corp.nutanix.com'
alias cot='ssh michael.haigh@cot02.corp.nutanix.com'
alias vb='sudo -b /Applications/VirtualBox.app/Contents/MacOS/VirtualBox'
alias cv='cd ~/caseview/; source ./bin/activate; cd sre-view/'
alias colo='cd ~/colo-automation; source ./bin/activate'
alias gshow='git log --graph --pretty=oneline --decorate --all'
alias devvm='ssh michael@10.4.100.128'
alias botvm='ssh centos@10.41.70.193'
alias dscp='michael@10.4.100.128:/home/michael/.'
alias jb='ssh michael@10.20.134.254'
alias cvp='ssh mhaigh@10.5.12.57'
alias cvd='ssh mhaigh@10.5.12.56'
alias s66='ssh nutanix@10.46.23.5'

# Nutanix Clusters
alias demopc='ssh nutanix@pc.nutanixdemo.com'
alias gpupc='ssh nutanix@10.45.5.30'
alias gpupe='ssh nutanix@10.45.5.12'
alias era='ssh era@10.45.5.40'
alias xipe='ssh -i ~/xiKeyPair nutanix@52.55.237.223 -p 2222'
alias xijb='ssh -i ~/xiKeyPair centos@3.81.252.156'
alias brandype='ssh nutanix@10.48.11.15'
alias brandypc='ssh nutanix@10.48.11.21'
alias daisypc='ssh nutanix@10.20.134.190'
alias daisy='ssh nutanix@10.20.132.100'
alias m92='ssh nutanix@10.20.92.29'
alias m94='ssh nutanix@10.20.94.29'
alias m94pc='ssh nutanix@10.20.94.39'
alias m233='ssh nutanix@10.42.233.37'
alias m233pc='ssh nutanix@10.42.233.39'
alias lonewolf='ssh nutanix@10.20.95.29'
alias lonewolfpc='ssh nutanix@10.20.95.38'
alias beastpc='ssh nutanix@10.4.220.196'
alias beast='ssh nutanix@10.4.220.64'
alias thing2='ssh nutanix@10.1.106.246'
alias thing2a='ssh nutanix@10.1.106.246'
alias thing2b='ssh nutanix@10.1.106.247'
alias thing2c='ssh nutanix@10.1.106.248'
alias thing2d='ssh nutanix@10.1.106.249'

function quit {
    osascript -e 'tell application "Terminal" to quit'
}

# python virtualenv stuff
source /usr/local/bin/virtualenvwrapper.sh
eval "$(direnv hook bash)"


# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/michael.haigh/Applications/google-cloud-sdk/path.bash.inc' ]; then . '/Users/michael.haigh/Applications/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/michael.haigh/Applications/google-cloud-sdk/completion.bash.inc' ]; then . '/Users/michael.haigh/Applications/google-cloud-sdk/completion.bash.inc'; fi
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CFLAGS="-I$(brew --prefix openssl)/include"
