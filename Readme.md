# Project Intro
Scraping of structured website of the Solar Impulse Foundation.

# What is Solar Impulse and why scrape it ?
SolarImpulse provides solutions data about many sectors, every solution can have organizations linked to it. This data is important for Buisnesses who have B2B (business-to-business) relation.

# Goal
The goal for this project is to scrape the data from the SolarImpulse website for two types of datasets:
(1) Solutions & Organizations
(2) Organizations Only

# Target Data
(1)[Solutions] Solution dataset URL,Solution name,Solution on-sentence summary,Identification,Label Date,By,From,Maturity stage,Looking For,Target client profile,Tags,Sectors,Youtube Video URL,The environmental benefits,The Financial benefits,Activity Region - Continent,Activity Region - Countries,Complementary solutions,Organization dataset URL

(2)[Organizations] Organization dataset URL,Organization name,Logo,Organization short description,Organization type,Founded,Company size,Member type,Founder 1 - First name,Founder 1 - Last name,Founder 2 - First name,Founder 2 - Last name,Founder 3 - First name,Founder 3 - Last name,Headquarters,Facebook profile link,Twitter profile link,LinkedIN profile link,Documents,About,Website link,SDG’s of application,Number of solutions

# Program Life cycle
You may notice some HTML Files within the files.
These are captured to avoid making new requests each time we would like to add new informtaions.