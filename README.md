# mihomo
> merge your clash subscription with custom file.

## Get start

```sh
docker start --name mihomo -d -p 8080:8080 -e SUBSCRIPTION_URL=xxxx marchocode/mihomo

# check your token.
docker exec mihomo cat /tmp/token

# your subscription url.
curl http://ip:port/sub/<your_token_here>
```