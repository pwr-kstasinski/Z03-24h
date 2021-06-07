wget -O swagger.json http://localhost:5000/spec
rm -rf client/apiclient
openapi-generator-cli generate
