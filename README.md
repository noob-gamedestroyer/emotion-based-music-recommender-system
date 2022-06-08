To run this project add `client_id`, `secret` and `username` in 
`application.properties` file.
 
* Username can be retrieved from account section in spotify app.

* also add the redirect-uri to developer console in edit settings option.

* and don't forget to add `application.properties` file to project root.

#### Format for `application.properties` file: 

* `[SpotifyCredentials]`
* `client_id = your_client_id`
* `client_secret = your_client_secret`
* `username = your_username`
* `redirect_uri = http://localhost:8080/callback`
