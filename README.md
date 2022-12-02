# Docker_Flask_Pipeline
Мой первый проект на библиотеках Docker, Flask и Pipeline. 
Итоговый проект курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy, Catboost  API: flask

Задача: предсказать по описанию клиента банка вероятность его ухода. Бинарная классификация

Используемые признаки:

Total_Trans_Amt
Total_Trans_Ct
Total_Relationship_Count
Total_Amt_Chng_Q4_Q1
Months_Inactive_12_mon
Total_Revolving_Bal 

Внутри пайплайна модели Churning_pipeline.dill генерируется еще 4 признака.

Клонируем репозиторий и создаем образ

$ git clone git@github.com:DAYa66/Docker_Flask_Pipeline.git 

$ cd Docker_Flask_Pipeline 

$ docker build -t DAYa66/Docker_Flask_Pipeline .

Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)

$ docker run -d -p 8180:8180 -v <your_local_path_to_pretrained_models>:/app/app/models DAYa66/Docker_Flask_Pipeline

Также приложены ноутбуки для проверки flask.
