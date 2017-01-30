# BCSMSSA Database Project

## Contributor requirements 
Contributors should have the following installed:  
1. Python 3.5 or greater  
2. Django   
3. Git

## Getting started
1. Create a directory for the project and cd into it
2. Run the following command to clone the repo  
``git clone https://github.com/CodeTheChangeUBC/bcsmssa.git``
3. cd into the project's directory and start the server with this command  
``python manage.py runserver``  
4. The project can now be accessed through a browser at  
``http://127.0.0.1:8000/``

## How to contribute
Note: If the change is only to a README file, commiting to the master branch will be fine  

1. Pick a task from the list of issues **OR** create a new issue if the task you want to complete is not listed 
2. Create a branch to work on the task in  
``git branch <name_of_branch>``
3. Switch into the new branch to begin work  
``git checkout <name_of_branch>``  
4. Implement the task
5. Pull from the master branch to get the lastest updates to the codebase  
``git pull origin master``
6. Resolve any merge conflicts, review and test code to be sure nothing has broken
8. Commit changes to your branch and checkout the master branch, then merge the feature and push to master  
After commiting changes:  
``git checkout master``  
``git merge <name_of_branch>``  
``git push origin master``
8. Close the issue on GitHub and delete the feature's branch if no more work will be done in it
