# BakeToSave
 This is a repository for our DIS-project

To run our application you need to:

    1. Run the following code to install requirements:
        $ pip install -r requirements.txt

    2. It is important you navigate to the src directory, to run the following code:
        $ python init_db.py

    3. Export flask:
        $ export FLASK_APP=app

    4. Run the application:
        $ flask run

----------------------------------------------------------------------------------------------------------------
Functionality of our application
 In our application you can find recipes depending on which ingredients are in it and what appliances are needed.

 You can use the search function to find recipes related to the name of the recipe, where we have used regular expression matching to make partial matching. This makes us able to find e.g. "bananbroed" even if we write it in two words as "banan broed". We have also made sure that danish letters; æ, ø, å, give results of ae, oe, aa respectively, so you can find smaakager, even though you search for småkager.

 We have checkboxes for ingredients, categories and appliances. Once you have selected, you can click done and it will update the page. The checkboxes remain checked, until you uncheck them or reset, as explained later. The appliance checkboxes removes recipes that have the checked appliance, where the two other removes all recipes that don't include the checked objects. Since a recipe can only have one category, we have used OR for the SQL query, so you get the recipes that match all the categories you have checked off. For ingredients you get the only the recipes that include first ingredient AND second ingredient, etc. You can combine the different checkboxes, but all checked objects will be reset, if you then try to use the search function, leave the front page, or click on the home button (BakeToSave) in the navigation bar.

 We also have two extra pages in the navigation bar; "About" and "Database Info", where you can read about the purpose of the website, as you would have on an actual website, as well as information on how we've made the database, and what that entails.