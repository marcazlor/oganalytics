# OGAnalytics — Definición del problema de Machine Learning (Fase 4)

## Contexto y usuario

Una refinería europea decide mensualmente su estrategia de aprovisionamiento de crudo: comprar Brent en el mercado local o importar WTI desde Estados Unidos. La importación es rentable cuando el diferencial Brent–WTI (spread) supera el coste del transporte transatlántico. Una predicción fiable del spread a un mes vista informa directamente esa decisión de compra, cuyo impacto económico, multiplicado por millones de barriles, es sustancial.

## Qué se predice

Se predice el **nivel del spread Brent–WTI mensual** (no su dirección ni su variación). Aunque predecir el nivel es más difícil que predecir la dirección, es lo que la decisión de negocio requiere: la refinería no necesita saber solo si el spread subirá o bajará, sino si su magnitud cubrirá el coste de transporte. La dirección sin magnitud no basta para decidir una importación.

## Horizonte

El horizonte de predicción es **un mes**. La justificación principal es de negocio: responde al ciclo de aprovisionamiento con el que las refinerías estructuran sus compras. Adicionalmente, coincide con la granularidad mensual de los datos del proyecto (precios resampleados, producción e inventarios mensuales), lo que evita reconstruir el pipeline de datos y mezclar frecuencias.

## Métricas de evaluación

La métrica principal es el **RMSE**. Se elige frente al MAE porque penaliza cuadráticamente los errores grandes, y en este caso de uso los errores grandes tienen costes desproporcionados: una predicción muy desviada puede inducir una decisión de importación equivocada (fletar crudo que no compensa, o renunciar a una importación que sí compensaba), cuyo coste no es proporcional al tamaño del error. El RMSE refleja mejor esa estructura de costes que el MAE.

Como métrica secundaria se reporta la **directional accuracy** (porcentaje de aciertos en la dirección del movimiento), porque acertar el sentido del cambio tiene valor propio para la decisión incluso cuando la magnitud predicha es imprecisa. Se reportará también el MAE como métrica complementaria de robustez, dado que la serie contiene outliers extremos conocidos (2008, 2020) a los que el RMSE es especialmente sensible.

## Baseline

El baseline principal es el **modelo naive de persistencia**: el spread del mes siguiente se predice igual al del mes actual. No requiere entrenamiento y es notoriamente difícil de batir en series financieras. Como baseline secundario se considera un modelo de **reversión a la media** (el spread converge hacia la media móvil de los últimos meses), coherente con la propiedad mean-reverting del spread identificada en la Fase 1.

Cualquier modelo de ML debe justificar su complejidad batiendo a estos baselines; en caso contrario, la complejidad añadida no aporta valor.

## Riesgos conocidos y sus implicaciones de diseño

El hallazgo central de la Fase 1 condiciona todo el diseño: el dataset del spread **no es estadísticamente homogéneo**. Contiene tres regímenes estructurales (pre-2011, 2011–2015, post-2015) gobernados por condiciones distintas (auge del shale, prohibición de exportación de crudo de EE. UU. y su levantamiento), y las relaciones entre variables cambian según el régimen: la relación inventarios de Cushing–spread, fuerte en 2011–2014, se desacopla a partir de 2016.

Implicaciones concretas para el diseño:

a) **Validación con TimeSeriesSplit**, nunca aleatoria: el orden temporal debe respetarse para no entrenar con información del futuro.
b) **Dummies de régimen o de eventos como features**, para que los modelos puedan capturar el cambio estructural.
c) **Evaluación por régimen además de global**: un resultado agregado puede ocultar que el modelo funciona en un régimen y falla en otro.
d) **Expectativa explícita de fallo en los cambios de régimen**: las transiciones entre regímenes son escasas en la serie (dos en cuarenta años), por lo que ningún modelo dispondrá de datos suficientes para aprenderlas. Se anticipa que los errores se concentrarán en esos puntos.

## Criterio de éxito y de fracaso

El modelo se considera útil si bate al baseline naive en RMSE **de forma consistente en la mayoría de las ventanas de validación temporal**, no solo en el agregado. Se evita fijar un umbral porcentual arbitrario; el criterio es la consistencia entre ventanas y entre regímenes.

Si ningún modelo bate al baseline de forma consistente, la conclusión del estudio no es un fracaso sino un hallazgo: con las features disponibles, el spread mensual no contiene señal explotable a este horizonte más allá de la persistencia. Documentar honestamente ese resultado tiene tanto valor como un modelo que funcione.

## Detección de anomalías

En paralelo al problema predictivo, se construirá un detector de anomalías (Isolation Forest) sobre el **spread**, elegido por ser la serie protagonista del proyecto. La validación será cualitativa contra los eventos conocidos de la Fase 1: el detector debe identificar como anómalos los episodios de 2008 (squeeze post-Lehman), 2011–2013 (régimen de spread extremo) y abril de 2020 (WTI negativo). La extensión del detector a las series de precios queda como mejora posterior.

## Alcance y presentación

El entregable de la fase se presenta como un **estudio comparativo de enfoques de forecasting** aplicados al spread (baseline naive → regresión lineal → Ridge → Gradient Boosting → XGBoost), con análisis de cuándo y por qué falla cada modelo, y no como "un modelo que predice el precio del petróleo". Esta framing es deliberada: refleja la dificultad real del problema y el valor analítico de entender los límites de la predicción.