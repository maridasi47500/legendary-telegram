
mkdir templates 
python3 scaffold.py user username email password country_id:references phone
python3 scaffold.py country name
python3 scaffold.py phonecall user_id grievous_situation_degree description place lat lon
python3 scaffold.py real_time_posting user_id title content social_media_reputation_risk:radio personal_relation_risk:radio lat lon roleplayer_id:references
python3 scaffold.py roleplayer name pic:file description
python3 scaffold.py plan_day_outdoor_activities user_id lat lon title description at_datetime
