SkLearn2PMML-Plugin
===================

The simplest way to extend [SkLearn2PMML] (https://github.com/jpmml/sklearn2pmml) package with custom transformation and model types.

# Features #

A template project with the following layout:
* `src/main/python` - Base directory for Python classes.
* `src/main/java` - Base directory for the corresponding Java classes.
* `src/main/resources/META-INF/sklearn2pmml.properties` - The mappings from Python classes to Java classes.

The example `com.mycompany.Aggregator` transformation implements "min", "max" and "mean" aggregation functionality in agreement with [PMML built-in functions "min", "max" and "avg"] (http://dmg.org/pmml/v4-3/BuiltinFunctions.html#min), respectively.

# Prerequisites #

* Python 2.7, 3.4 or newer.
* Java 1.7 or newer.

# Installation #

Enter the project root directory and build using [Apache Maven] (http://maven.apache.org/):
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
from com.mycompany import Aggregator

iris_pipeline = PMMLPipeline([
	("mapper", DataFrameMapper([
		(["Sepal.Length", "Petal.Length"], [ContinuousDomain(), Aggregator(function = "mean")]),
		(["Sepal.Width", "Petal.Width"], [ContinuousDomain(), Aggregator(function = "mean")])
	])),
	("classifier", LogisticRegression())
])
iris_pipeline.fit(iris_df, iris_df["Species"])
```

Export the example pipeline to a PMML file. Use the `user_classpath` attribute to specify the location of the JAR file:
```Python
from sklearn2pmml import sklearn2pmml

sklearn2pmml(iris_pipeline, "Iris.pmml", user_classpath = ["/path/to/sklearn2pmml-plugin/target/sklearn2pmml-plugin-1.0-SNAPSHOT.jar"])
```

If the PMML file is opened in text editor, then it is possible to see that the `TransformationDictionary` element has been populated with two `DerivedField` elements that correspond to the `com.mycompany.Aggregator` transformation:
```XML
<TransformationDictionary>
	<DerivedField name="avg(Sepal.Length, Petal.Length)" optype="continuous" dataType="double">
		<Apply function="avg">
			<FieldRef field="Sepal.Length"/>
			<FieldRef field="Petal.Length"/>
		</Apply>
	</DerivedField>
	<DerivedField name="avg(Sepal.Width, Petal.Width)" optype="continuous" dataType="double">
		<Apply function="avg">
			<FieldRef field="Sepal.Width"/>
			<FieldRef field="Petal.Width"/>
		</Apply>
	</DerivedField>
</TransformationDictionary>
```

# License #

SkLearn2PMML-Plugin is licensed under the [GNU Affero General Public License (AGPL) version 3.0] (http://www.gnu.org/licenses/agpl-3.0.html). Other licenses are available on request.

# Additional information #

Please contact [info@openscoring.io] (mailto:info@openscoring.io)
