SkLearn2PMML-Plugin
===================

The simplest way to extend [SkLearn2PMML](https://github.com/jpmml/sklearn2pmml) package with custom transformation and model types.

# Features #

A template project with the following layout:
* `src/main/python` - Base directory for Python classes.
* `src/main/java` - Base directory for the corresponding Java classes.
* `src/main/resources/META-INF/sklearn2pmml.properties` - The mappings from Python classes to Java classes.

Example transformer classes:
* `com.mycompany.Aggregator`. Implements "min", "max" and "mean" aggregation functionality in agreement with [PMML built-in functions "min", "max" and "avg"](http://dmg.org/pmml/v4-3/BuiltinFunctions.html#min), respectively.
* `com.mycompany.PowerFunction`. Implements power function in agreement with the [PMML built-in function "pow"](http://dmg.org/pmml/v4-3/BuiltinFunctions.html#math).
* `com.mycompany.StringNormalizer` - Implements string normalization (conversion to lower/uppercase followed by trimming whitespace) in agreement with [PMML built-in functions "uppercase", "lowercase" and "trimBlanks"](http://dmg.org/pmml/v4-3/BuiltinFunctions.html#uppercase).

# Prerequisites #

* Python 2.7, 3.4 or newer.
* Java 1.7 or newer.

# Installation #

Enter the project root directory and build using [Apache Maven](http://maven.apache.org/):
```
mvn clean install
```

The build produces an EGG file `target/sklearn2pmml_plugin-1.0rc0.egg` and a JAR file `target/sklearn2pmml-plugin-1.0-SNAPSHOT.jar`.

# Usage #

Add the EGG file to the `PYTHONPATH` environment variable:
```
export PYTHONPATH=$PYTHONPATH:/path/to/sklearn2pmml-plugin/target/sklearn2pmml_plugin-1.0rc0.egg
```

Fit an example pipeline:
```Python
import pandas

iris_df = pandas.read_csv("Iris.csv")

from sklearn2pmml import PMMLPipeline
from sklearn2pmml.decoration import ContinuousDomain
from sklearn_pandas import DataFrameMapper
from sklearn.linear_model import LogisticRegression
from com.mycompany import Aggregator, PowerFunction

iris_pipeline = PMMLPipeline([
	("mapper", DataFrameMapper([
		(["Sepal.Length", "Petal.Length"], [ContinuousDomain(), Aggregator(function = "mean")]),
		(["Sepal.Width", "Petal.Width"], [ContinuousDomain(), PowerFunction(power = 2)])
	])),
	("classifier", LogisticRegression())
])
iris_pipeline.fit(iris_df, iris_df["Species"])
```

Export the example pipeline to a PMML file. Use the `user_classpath` argument to specify the location of the JAR file:
```Python
from sklearn2pmml import sklearn2pmml

sklearn2pmml(iris_pipeline, "Iris.pmml", user_classpath = ["/path/to/sklearn2pmml-plugin/target/sklearn2pmml-plugin-1.0-SNAPSHOT.jar"])
```

The PMML representation of transformers varies depending on the "composition" of the pipeline. In the example example, the `com.mycompany.Aggregator` transformer is represented as a `DerivedField` element, whereas the `com.mycompany.PowerFunction` transformer is represented as a `NumericPredictor@exponent` attribute:
```XML
<PMML xmlns="http://www.dmg.org/PMML-4_3" version="4.3">
	<TransformationDictionary>
		<DerivedField name="avg(Sepal.Length, Petal.Length)" optype="continuous" dataType="double">
			<Apply function="avg">
				<FieldRef field="Sepal.Length"/>
				<FieldRef field="Petal.Length"/>
			</Apply>
		</DerivedField>
	</TransformationDictionary>
	<RegressionModel functionName="classification" normalizationMethod="softmax">
		<MiningSchema>
			<MiningField name="Species" usageType="target"/>
			<MiningField name="Sepal.Width"/>
			<MiningField name="Petal.Width"/>
			<MiningField name="Sepal.Length"/>
			<MiningField name="Petal.Length"/>
		</MiningSchema>
		<RegressionTable intercept="0.15312185052146582" targetCategory="setosa">
			<NumericPredictor name="avg(Sepal.Length, Petal.Length)" coefficient="-1.5862823598313542"/>
			<NumericPredictor name="Sepal.Width" exponent="2" coefficient="0.864623482260917"/>
			<NumericPredictor name="Petal.Width" exponent="2" coefficient="-1.7337433442275574"/>
		</RegressionTable>
		<RegressionTable intercept="-0.41196434155188394" targetCategory="versicolor">
			<NumericPredictor name="avg(Sepal.Length, Petal.Length)" coefficient="1.6174796043315152"/>
			<NumericPredictor name="Sepal.Width" exponent="2" coefficient="-0.5854978099617918"/>
			<NumericPredictor name="Petal.Width" exponent="2" coefficient="-1.4870454407048939"/>
		</RegressionTable>
		<RegressionTable intercept="-1.0913325888211003" targetCategory="virginica">
			<NumericPredictor name="avg(Sepal.Length, Petal.Length)" coefficient="-0.3554755078012205"/>
			<NumericPredictor name="Sepal.Width" exponent="2" coefficient="-0.569705884824069"/>
			<NumericPredictor name="Petal.Width" exponent="2" coefficient="2.9003699714343223"/>
		</RegressionTable>
	</RegressionModel>
</PMML>
```

# License #

SkLearn2PMML-Plugin is licensed under the [GNU Affero General Public License (AGPL) version 3.0](http://www.gnu.org/licenses/agpl-3.0.html). Other licenses are available on request.

# Additional information #

Please contact [info@openscoring.io](mailto:info@openscoring.io)
