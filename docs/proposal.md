## Data Engineering Project Proposal

Due in large part to the pandemic causing a surge in demand for computer components due to work from home and study from home. As well as crippling normal operations for manufacturers, components are not harder to get than ever.

Even when components are available they are being purchased online within a matter of seconds, not minutes. To help combat this providing a tool for non-technical consumers would help give them a chance to at least be able to add a desired item to their shopping carts.

#### Question/need:
* What is the framing question of your analysis, or the purpose of the model/system you plan to build? 
    - To provide subscribers with stock notifications for in demand tech, which not natively availabe on existing platforms.
    - To predict possible upcoming release dates and time based on past release schedules.
* Who benefits from exploring this question or building this model/system?
    - "Normal" shoppers needing a way to combat bots and scalpers. 

#### Data Description:
* What dataset(s) do you plan to use, and how will you obtain the data?
    - Scraped sites
        - Best Buy
        - Amazon
        - Newegg
        - Microcenter
* What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with?
    - Name of product
    - Category
    - Subcategory
    - Vendor
    - Datetime of availability
    - Item types
        - Combos
        - Individual
    - Price
* If modeling, what will you predict as your target?
    - Possible future releases
        - Category
        - Date
        - Time

#### Tools:
* How do you intend to meet the tools requirement of the project? 
    - Scraping Tools
        - Requests
        - BeautifulSoup
        - Selenium
    - Storage
        - Postgres
    - Notifications
        - Discord
* Are you planning in advance to need or use additional tools beyond those required?
    - Discord
        - Bot
        - Community channel

#### MVP Goal:
* What would a [minimum viable product (MVP)](mvp.md) look like for this project?
    - Having all the scrapers running autonomously and inserting valid records into a database.