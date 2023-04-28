# Test Cases Summary

|     | Test                                                                                                                                                                                       | Link                                                                                                                                    |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Test database**: should be able to connect to and access the database                                                                                                                    | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/15/workflows/86ee07d5-0a16-47f8-97d8-069940341ef5/jobs/15 |
| 2   | **Test get all wishlists - empty**: should return a empty list with a status code 200 when no record existing in the database                                                              | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/24/workflows/ff54a385-2e6f-45e3-824d-1b160482645d/jobs/24 |
| 3   | **Test create new empty wishlist**: should return an error message “Error: Invalid input” with a status code 400                                                                           | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/28/workflows/19ad19cd-2736-4b3f-9c99-836b041bc4e8/jobs/26 |
| 4   | **Test create new wishlist**: should return a success message “Success: New wishlist added!” with a status code 201 & record that query by destination should match the corresponding date | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/29/workflows/904e347e-5239-4ced-864b-b68fe6701863/jobs/27 |
| 5   | **Test create existing wishlist**: should return a success message “Success: Wishlist updated!” with a status code 201 & record that query by destination should match the updated date    | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/30/workflows/ae721fc4-c800-4a5d-ac9b-01979d39441a/jobs/28 |
| 6   | **Test get all wishlists**: should return a list of json with a status code 200                                                                                                            | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/31/workflows/4d5ac921-4bdd-4745-9523-339075332a68/jobs/29 |
| 7   | **Test get an non-existing single wishlist**: should return a status code 204                                                                                                              | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/32/workflows/761054a1-6385-456c-9ed0-f62b3ce0099d/jobs/30 |
| 8   | **Test get a single wishlist**: should return a corresponding json object with a status code 200                                                                                           | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/33/workflows/35396821-7b87-41fe-bc3e-2bddcac4f7e8/jobs/31 |
| 9   | **Test update a single wishlist - invalid input**: should return an error message “Error: Invalid input” with a status code 400                                                            | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/34/workflows/9af4dc83-3f65-410f-920e-2f1b41c607aa/jobs/32 |
| 10  | **Test update a single wishlist - existing**: should return a success message “Success: Wishlist updated!” with a status code 201                                                          | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/36/workflows/24f46a9e-608a-4cab-9a35-401ca2596f58/jobs/34 |
| 11  | **Test update a single wishlist - nonexisting**: should return a status code 204                                                                                                           | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/37/workflows/a8ea4816-323c-4a7f-a24c-7d8e4629102f/jobs/35 |
| 12  | **Test delete a single wishlist - existing**: should return a success message “Success: Wishlist deleted!” with a status code 202                                                          | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/38/workflows/c24322a8-3ff1-4e5c-8fec-c8ef886da781/jobs/36 |
| 13  | **Test delete a single wishlist - nonexisting**: should return a status code 204                                                                                                           | https://app.circleci.com/pipelines/github/Gitcatmeoww/goTravel-build-and-test/39/workflows/d151fa4a-4d88-4f1d-abd6-4b823cdc2b4d/jobs/37 |