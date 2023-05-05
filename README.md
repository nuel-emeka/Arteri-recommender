# Health Insurance Recommendation Engine for Nigeria

This is a pioneering application of recommender systems in health insurance in Nigeria, aiming to improve the accessibility and decision-making process of selecting Health Management Organizations (HMOs) and their plans.

## Background

Despite the importance of health insurance in Nigeria, its adoption rate remains low. To address this, efforts to raise awareness, facilitate access to information, and provide decision-making tools are crucial. AI-powered recommender systems, which have gained popularity in various domains, are employed to assist users in finding the right HMO and plan for their needs.

HMOs serve as agents of the National Health Insurance Scheme (NHIS) and offer health insurance coverage to both private and public sectors. Currently, there are 58 NHIS-accredited HMOs in Nigeria, offering a total of 155 plans. These plans differ in aspects such as price, benefits, geographical coverage, and value-added options, making the selection process quite complex.

## Approach

We utilized a content-based recommender system that offers greater accuracy and efficiency, as it can be implemented offline and is non-dynamic, unlike user-based methods. The system was developed using the Cosine Similarity algorithm, which outperformed the KNN algorithm in our evaluations.

### Algorithm Performance Evaluation

Our experienced team of medical and domain experts assessed the algorithm's performance by comparing the recommendations provided by both the Cosine Similarity and KNN algorithms. We input various user choices into the recommender systems and examined the resulting recommendations. It was determined that the Cosine Similarity algorithm provided the most accurate recommendations, as most users already on insurance plans were recommended their current HMOs after inputting their needs.

## How it Works

The Arteri-Recommender system considers user preferences and filters HMO data based on location and price range. It then recommends the top 5 HMOs with the closest similarity in services offered according to the user's preferences, and then filters down to 3 based on existing ratings.

# Data and other resources
We have added the data used in developing this algorithm including the raw data we collected. This will need to be updated and edited to reflect present realities and state of the industry.
The HMO ratings file is a publicly aggregated feedback of some of the available HMOs which was applied to filter the final recommendation to the user.


# Development Team 
Emmanuel Nnaemeka - Lead ML Engineer 

Ayomide Owoyemi - Product Manager, ML Engineer & medical domain expert

Daniel Eloghosa Irowa-Omoregie - Medical domain expert

Olukoya O. Fatosa - SWE

Kenechukwu Jane Iloegbunam - Data Engineer

Abdulrasheed Lawal - SWE

Morountonu Oluwaseyi - Project Manager

Abubakar Omolaja - SWE

Ronald Ikpe - Medical domain expert

Wuraola Oyewusi - Advisor

Temitope Isedowo - SWE


## For enquiries and clarifications 
Reach out to Emmanuel (emmanuelnnaemeka847@gmail.com) or Ayo (blacbard@gmail.com)
