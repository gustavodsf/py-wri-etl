# py-wri-etl

> coonect to sql server

```sh
sqlcmd -C  -S tcp:127.0.0.1,1433 -U sa -P mssql1Ipw
```

> create user and secret key

```sql
CREATE LOGIN GFWProUser WITH PASSWORD = 'measure2010!';
create user GFWProUser for login GFWProUser;
EXEC sp_addrolemember N'db_datawriter', N'GFWProUser';
EXEC sp_addrolemember N'db_datareader', N'GFWProUser';
GRANT EXECUTE TO GFWProUser;
EXEC master..sp_addsrvrolemember @loginame = N'GFWProUser', @rolename = N'sysadmin';
```

> Docker command to create sql server container

```sh
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=R@@t123456" \                                
   -p 1433:1433 --name sql1 --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest
```

> create a network

```sh
docker network create gfwpro-network
```