# API Assignment

This is an assignment to create an API with 3 different implementations. It is developed using Django.

It is an API with three main URL.

### Whereever there is an <int> in the url you are supposed to replace it with the user_id

## `\normal\` - Implementation of ORM on PostgresSQL database. 
- It has 4 defined methods - get, post, put, delete.
- For `get` method use `\normal\<int>` to get the data of a single user, or don't add any integer at the end of the url to fetch all the users from the table.
- For `post` method pass the data to the url as the request body according to the model to url `\caching\`.
- For `put` method pass the data to the url just as the `post` method but only provide data for the attribute which is to be updated and put `null` as the value for other attributes.
- For 'delete' method use `\normal\<int>`.

## `\caching\` - Implementation of caching
- It also has 4 defined methods - get, post, put, delete.
- For `get` method use `\caching\<int>` to get the data of a single user.
- For `post` method pass the data to the url as the request body according to the model to url `\caching\`.
- For `put` method pass the data to the url `\caching\<int>` just as the `post` method but only provide data for the attribute which is to be updated and put `null` as the value for other attributes.
- For 'delete' method use `\caching\<int>`. This will only delete the data from cache to delete the data from the database use delete method with Normal API.

## `\sharding\` - Impplementation of sharding
- It has 2 previous API defined for it with sharding implemented in them.
- Both the API's havs 4 defined methods - get, post, put, delete.
- The URL for them will be `\sharding\normal\` to access the Normal API inside the Sharding API and `\sharding\caching\` to access the Caching API inside the Sharding API.
- For `get` method use `\sharding\caching\<int>` or `\sharding\caching\<int>` to get the data of a single user or don't add any integer at the end of the url to fetch all the users from the table, this doesn't work for the Caching API.
- For `post` method pass the data to the url as the request body according to the model to url `\sharding\caching\` or `\sharding\caching\`.
- For `put` method pass the data to the url `sharding\normal\<int>` or `sharding\caching\<int>` just as the `post` method but only provide data for the attribute which is to be updated and put `null` as the value for other attributes.
- 'delete' method with url `sharding\normal\<int>` will delete the user from the database but with url `sharding\caching\<int>` will delete the user from the cache.
