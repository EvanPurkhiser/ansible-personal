#!/bin/sh

# All secrets for my personal machine configurations are stored in my personal
# 1password vault. This automatically extracts them.

# Access point credentials
echo wifi_password=\'"$(
    op get item 'pscarwpmj5bqpf57rqv4gfrsjq' | \
        jq -r '.details.sections[].fields[]? | select(.n == "wireless_password").v'
)"\'

# Transmission RPC API HTTP password
echo transmission_rpc_password=\'"$(
    op get item 'er47ejg7jjcgxh3ztyvzlsrlzy' | \
        jq -r '.details.fields[] | select(.name == "password").value'
)"\'

# Cloudflare DNS credentials
echo cloudflare_email=\'"$(
    op get item 'z7qz2rxy6rb4xphfzmktsnauv4' | \
        jq -r '.details.fields[] | select(.name == "username").value'
)"\'

echo cloudflare_token=\'"$(
    op get item 'z7qz2rxy6rb4xphfzmktsnauv4' | \
        jq -r '.details.sections[].fields[]? | select(.n == "B12E0ECF27AC4357B784CCF59A455C49").v'
)"\'

# Backup solution encryption and access token
echo rclone_backup_key=\'"$(
    op get item 'rzki4bpthbcx3dvunjvect545e' | jq -r '.details.password'
)"\'

echo rclone_backup_salt=\'"$(
    op get item 'rzki4bpthbcx3dvunjvect545e'| \
        jq -r '.details.sections[].fields[]? | select(.n == "C1C73CD15D304C168BA41338A0792881").v'
)"\'

echo rclone_gdrive_token=\'"$(
    op get item 'rzki4bpthbcx3dvunjvect545e'| \
        jq -r '.details.sections[].fields[]? | select(.n == "A36E5CA6867D4AE385AAC496F302535B").v'
)"\'
