# NurtureLabsAssignment

completed my assignement using python-flask as framework.
used mongodb for databases.
used json format.

Deployed in heroku https://srikanthbs.herokuapp.com/ and tested using postman. Screenshots of postman is also uploaded.

And also deployed in repl.it.

API'S documentation

1. admin: add an advisor
https://srikanthbs.herokuapp.com/admin/advisor/

json request example: 
{
    "advisor_name":"xyz",
    "advisor_photo_url":"/pics/xyz.png"
}

2. user: register
https://srikanthbs.herokuapp.com/user/register/

json request example:
{
    "name":"ppp",
    "email":"ppp@gmail.com",
    "password":"sri974213"
}

3. user: login
https://srikanthbs.herokuapp.com/user/login/
{
    "email":"john@gmail.com",
    "password":"sri974213"
}

4. user: list of advisor
https://srikanthbs.herokuapp.com/user/userid/advisor
eg:-
https://srikanthbs.herokuapp.com/user/john14/advisor

    
5. user: book call with an advisor
https://srikanthbs.herokuapp.com/user/userid/advisor/<advisorid>
eg:-
https://srikanthbs.herokuapp.com/user/john14/advisor/sri3   

{
    "booking_time":"2021-10-25 15:12:30"
}

6. user: get all the booked calls
https://srikanthbs.herokuapp.com/user/userid/advisor/booking/
eg:
https://srikanthbs.herokuapp.com/user/john14/advisor/booking/
