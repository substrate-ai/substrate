# Python-backend

This is mainly used when the supabase based backend cannot support a use case.
Right now it is mainly used for the aws-sdk to control our user job in the cloud

The python backend use fast-api to serve the API 

To run 
`cd src; uvicorn main:app --reload`

Production logs can be found on deta.space

To deploy the updated code into production
`space push`
