Technical Contributions

One of my primary responsibilities in this project was setting up the APIs for data collection, specifically FIDE, Chess.com, and SERPAPI. My prior experience with these APIs allowed me to quickly navigate authentication keys, understand rate limits, and efficiently extract relevant data. Since I was already familiar with the structure of the available data, I could anticipate potential challenges and streamline the collection process.

Initially, I drafted the first set of functions designed to pull JSON data from these APIs. However, as the project evolved, we realized that working directly with JSON made database integration more cumbersome. To improve efficiency, we transitioned to using Pandas DataFrames and CSV files, which facilitated smoother database construction. I played a key role in adapting our data collection methods to this new approach, helping to refine and optimize the updated functions.

Beyond data collection, I also took the lead in designing and iterating the chess.db database. Since our dataset changed throughout the project—initially relying on raw JSON but later incorporating structured CSV and DataFrame formats—I had to continuously adjust the database schema. I experimented with different ways to structure the tables, ensuring that our design could accommodate timeseries data effectively. Through this process, I gained valuable experience in database organization, particularly in handling timeseries data and leveraging data melting techniques to make our database more flexible.

Another significant contribution I made was developing the visualizations for comparing Google Trends data with FIDE rating progressions. This required me to learn and apply the Plotly library, which I used to create interactive graphs that provided a clearer representation of our findings. The ability to explore the data dynamically helped us better understand correlations between player popularity and their performance metrics.

Team Collaboration

I’m happy to say that our team successfully met several times throughout the project duration and achieved meaningful progress in these meetings. Our team held each other accountable and shared the spread of work equally, with no one person disproportionately taking on more work

A specific challenge we faced early on was how to efficiently structure the data collection process. During the Christmas break, I worked independently to complete the initial version of our Data Collection notebook. While my first implementation was functional, it wasn’t as streamlined as it could have been. Fortunately, my teammates provided valuable feedback, and together, we iteratively refined the data collection methods. This experience highlighted the importance of collaboration—even if an individual approach works, incorporating diverse perspectives can lead to a much more optimized solution.

One area where I could have improved was in my level of communication. Since this project spanned an extended period, there were moments when I wasn’t as engaged as I could have been. In retrospect, making a more consistent effort to check in and discuss our collective direction would have helped keep everyone aligned, especially myself.

Learning Journey

One of the biggest technical skills I developed during this project was improving my ability to collect, store, and manipulate data efficiently. While I had previous experience with API requests, this project challenged me to integrate multiple data sources into a cohesive database while considering long-term scalability (IE everything FIDE). I also deepened my understanding of working with timeseries data, particularly in how to structure and melt datasets to maximize flexibility.

Additionally, learning Plotly was a valuable experience. Before this project, I had primarily used Matplotlib and Seaborn for data visualization. However, Plotly’s interactive capabilities provided a much richer way to analyze our findings. Becoming proficient in this library has broadened my toolkit for future data visualization tasks.
On a personal level, this project reinforced the importance of adaptability. We encountered several points where our initial approach wasn’t the most efficient, requiring us to pivot and rework parts of our codebase (primarily NB01 and NB02). 

For future growth, one of my main goals is to improve my communication with teammates. While I contributed significantly to the technical aspects, I recognize that being an effective team member goes beyond writing good code—it also involves actively engaging with discussions, providing feedback on others’ work, and ensuring that we maintain a shared vision. Additionally, I want to be more mindful of balancing individual work with team collaboration. While my eagerness to make quick progress over the break was well-intentioned, I realized that working too independently can sometimes lead to inefficiencies that could be avoided through more collaborative efforts.
