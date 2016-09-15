firewall-cmd --set-default-zone=public
firewall-cmd --permanent --remove-port=9200/tcp
firewall-cmd --permanent --remove-port=9300/tcp
firewall-cmd --permanent --zone=public --add-rich-rule="rule family="ipv4" source address="$1" port protocol="tcp" port="9200" accept"
firewall-cmd --permanent --zone=public --add-rich-rule="rule family="ipv4" source address="$1" port protocol="tcp" port="9300" accept"
firewall-cmd --reload
