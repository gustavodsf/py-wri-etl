# py-wri-etl

> coonect to sql server

```sh
sqlcmd -C  -S tcp:127.0.0.1,1433 -U sa -P R@@t123456
```

> create user and secret key

```sql
CREATE LOGIN GFW****** WITH PASSWORD = '######';
create user GFW****** for login GFW******
EXEC sp_addrolemember N'db_datawriter', N'GFW******'
EXEC sp_addrolemember N'db_datareader', N'GFW******'
```

> Docker command to create sql server container

```sh
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=R@@t123456" \                                
   -p 1433:1433 --name sql1 --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest
```