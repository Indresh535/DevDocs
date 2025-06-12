from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
data = assembler.transform(df)

lr = LinearRegression(featuresCol="features", labelCol="label")
model = lr.fit(data)
