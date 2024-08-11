# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Fix Java issue
export _JAVA_AWT_WM_NONREPARENTING=1

# ZSH AutoSuggestions Plugin
if [ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# ZSH Syntax Highlighting Plugin
if [ -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
    source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# ZSH AutoComplete Plugin
if [ -f /usr/share/zsh-autocomplete/zsh-autocomplete.plugin.zsh ]; then
    source /usr/share/zsh-autocomplete/zsh-autocomplete.plugin.zsh
fi

function settarget(){
  ip_address=$1
  machine_name=$2
  echo "$ip_address $machine_name" > /home/parrot/.config/bin/target
}

function cleartarget(){
  echo "" > /home/parrot/.config/bin/target
}

function mkt(){
	mkdir {nmap,content,exploits,scripts}
}

function extractPorts(){
  orts="$(cat $1 | grep -oP '\d{1,5}/open' | awk '{print $1}' FS='/' | xargs | tr ' ' ',')"
  ip_address="$(cat $1 | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort -u | head -n 1)"
  echo -e "\n[*] Extracting information...\n" > extractPorts.tmp
  echo -e "\t[*] IP Address: $ip_address"  >> extractPorts.tmp
  echo -e "\t[*] Open ports: $ports\n"  >> extractPorts.tmp
  echo $ports | tr -d '\n' | xclip -sel clip
  echo -e "[*] Ports copied to clipboard\n"  >> extractPorts.tmp
  cat extractPorts.tmp; rm extractPorts.tmp
}

# Custom Aliases
# bat
alias cat='bat'
alias catn='bat --style=plain'
alias catnp='bat --style=plain --paging=never'

# ls
alias ll='lsd -lh --group-dirs=first'
alias la='lsd -a --group-dirs=first'
alias l='lsd --group-dirs=first'
alias lla='lsd -lha --group-dirs=first'
alias ls='lsd --group-dirs=first'

# burpsuite
alias bs='/usr/bin/burpsuite 2>/dev/null & disown'

# History
HISTFILE=$HOME/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt histignorealldups sharehistory

xset r rate 250 25

source /home/user/powerlevel10k/powerlevel10k.zsh-theme

export PATH=/usr/sbin/john:$PATH

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh