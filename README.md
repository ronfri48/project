# How to run the MUD Environment

1. git clone https://github.com/ronfri48/project.git or extract the code from the given zip

2. change cwd to /mudproject

3. Run copy_config_files.sh, and if you have any problem run sudo chmod +x copy_config_files.sh before

4. Run 
   * sudo check_faucet_config /etc/faucet/faucet.yaml
   * sudo systemctl reload faucet
   * sudo mn --nat --controller=remote

5. Check that everything configured by running in mininet shell the following commands:
    * h1 ping 8.8.8.8
    * h1 ping h2
    * h2 ping 10.0.0.1
    * h2 ping 8.8.8.8

6. Run in mininet shell the following commands: 
    * xterm h1 h2 h2 h2
        * In the first h2 shell run run_dns_sniffer.sh, and if you have any problem run sudo chmod +x run_dns_sniffer.sh before
        * In the second h2 shell run run_server.sh , and if you have any problem run sudo chmod +x run_server.sh before
        * In the third h2 shell run -
            * sudo python3 upload_mud.py show/huebulbmud.json
            * sudo python3 upload_mud.py show/wemoswitchmud.json
        * In h1 shell run - 
            * If tcpreplay is missing run sudo apt-get install tcpreplay
            * sudo tcpreplay -i h1-eth0 -t show/Setup-A-3-STA.pcap
            * sudo tcpreplay -i h1-eth0 -t show/uk_reg.pcapng
