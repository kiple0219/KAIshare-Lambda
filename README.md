
### Database Connection  
  - Host : kaishare-db.c61emr7whdod.ap-northeast-2.rds.amazonaws.com  
  - Port : 3306  
  - Username : admin  
  - Password : team7800  

### API Index
- signin
  - POST : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/signin
- login
  - POST : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/login
- post
  - {category}
    - GET : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}
    - POST : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}
    - {p_id}
      - GET : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}
      - PATCH : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}
      - DELETE : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}
      - join
        - POST : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/join
      - leave
        - POST : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/leave
      - close
        - PATCH : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/close
      - disable
        - PATCH : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/disable
      - share
        - GET : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/share
      - comment
        - POST : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/comment
        - {c_id}
          - PATCH : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/comment/{c_id}
          - DELETE : https://10x53vstw6.execute-api.ap-northeast-2.amazonaws.com/production/post/{category}/{p_id}/comment/{c_id}