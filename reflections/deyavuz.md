**Technical Contributions**

One technical problem I tackled by myself was dealing with the unnesting of Chess.com and FIDE JSON data. The initial data we gathered was incredibly noisy, confusing, and nested, to an extent that it was unusable without extensive processing and cleaning. I tasked myself with resolving this issue, as it was important to us to have clean, accessible data, alongside a streamlined data collection method. Thus, I adapted our previous code, which saved all of our nested raw JSONs, and instead wrote code which would save those dataframes as objects and converted them into pandas dataframes, from which I then created two single CSV files, one for Chess.com and one for FIDE data. This made our entire data collection and creating an SQL database process easier, cleaner, and more streamlined. 

The main contribution I made is NB03 - Data Analysis. I analysed, plotted, and commented on the FIDE and Chess.com data using the letsplot library to create interactive plots that show the differences in game modes, rating progressions, and online vs. over-the-board ratings. I performed exploratory analysis using this specific data, by using our initial questions as a starting point and commenting on the findings. 

Additionally, as I like figuring out different methods of playing around with aesthetics and visual displays, I edited and polished most of our work on the README file, to format it in a way that is more legible and cohesive, specifically by creating a linked Table of Contents and Order of Notebooks table.

I also created the functions.py file and transferred all of our functions there, for clarity, and imported them in the necessary files.

**Team Collaboration**

Our team was on top of things, both in terms of keeping in touch and updating each other, and getting actual work done on our repository. Thus, thankfully, we didn't have to take any conflict resolution steps. I believe we demonstrated a good example for team communication and collaborative, respectful group discussion and work. 

We shared the workload of booking and attending office hours; while I attended an office hour to discuss our plans and ideas while my teammates were busy during the exam period, we divided the workload equally for the rest of the assignment.

**Learning Journey**

Primarily, working on this assignment significantly helped me develop my Git version control skills. Aside from learning how to collaborate on a social and communication-level, this assignment taught me valuable skills about branching, merging, and working locally and contributing to a common repository, which I believe will be very useful in my career. Additionally, I got quite profficient working with pandas for this assignment, as after my team members wrote the initial functions to retreive the data from the web scraper and APIs, I streamlined the code by applying a pandas frame to it, converting our data to CSV files without saving them separately as JSONs. Most importantly, I learned how to work within a team on a data science task, which has provided very helpful, as I am now doing another group project for my second data science module, DS202A and applying my newfound skills there.

However, my learning journey had its obstacles, specifically within managing Git branches and merges. Although at first it seemed simple to work on separate branches and push to main as we worked on our notebooks, this process proved tougher as we progressed. Especially towards the end of our project, when our work ceased to be fragmanted and we were all working on our main branch, directly editing, deleting, and contributing to one another's code, I had to do considerable research online, while also reading through my team members' commit history, so to not override any of our work. Although tough, this proved to be invaluable experience, as I am already utilizing these skills, as I've previously mentioned, in my DS202 group project. 

One thing we could have improved as a group is time management: although we are satisfied with our final product, we could have set more internal deadlines to ensure the workload was distributed evenly throughout the month. In following projects, this could be improved upon.