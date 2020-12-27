class DCN(tfrs.Model):
    
    def __init__(self, use_cross_layer, deep_layer_sizes, projection_dim=None, str_features, int_features):
        super().__init__()

        self.embedding_dimension = 32

#         str_features = ["movie_id", "user_id", "user_zip_code",
#                         "user_occupation_text"]
#         int_features = ["user_gender", "bucketized_user_age"]

        self._all_features = str_features + int_features
        self._embeddings = {}

        # Compute embeddings for string features.
        for feature_name in str_features:
            vocabulary = vocabularies[feature_name]
            self._embeddings[feature_name] = tf.keras.Sequential(
                [tf.keras.layers.experimental.preprocessing.StringLookup(
                    vocabulary=vocabulary, mask_token=None),
                 tf.keras.layers.Embedding(len(vocabulary) + 1,
                                           self.embedding_dimension)
                ])

        # Compute embeddings for int features.
        for feature_name in int_features:
            vocabulary = vocabularies[feature_name]
            self._embeddings[feature_name] = tf.keras.Sequential(
              [tf.keras.layers.experimental.preprocessing.IntegerLookup(
                  vocabulary=vocabulary, mask_value=None),
               tf.keras.layers.Embedding(len(vocabulary) + 1,
                                         self.embedding_dimension)
              ])

        if use_cross_layer:
            self._cross_layer = tfrs.layers.dcn.Cross(
              projection_dim=projection_dim,
              kernel_initializer="glorot_uniform")
        else:
            self._cross_layer = None

        self._deep_layers = [tf.keras.layers.Dense(layer_size, activation="relu")
          for layer_size in deep_layer_sizes]

        self._logit_layer = tf.keras.layers.Dense(1)

        self.task = tfrs.tasks.Ranking(
          loss=tf.keras.losses.MeanSquaredError(),
          metrics=[tf.keras.metrics.RootMeanSquaredError("RMSE")]
        )

    def call(self, features):
        # Concatenate embeddings
        embeddings = []
        for feature_name in self._all_features:
            embedding_fn = self._embeddings[feature_name]
            embeddings.append(embedding_fn(features[feature_name]))

        x = tf.concat(embeddings, axis=1)

        # Build Cross Network
        if self._cross_layer is not None:
            x = self._cross_layer(x)

        # Build Deep Network
        for deep_layer in self._deep_layers:
            x = deep_layer(x)

        return self._logit_layer(x)

    def compute_loss(self, features, training=False):
        labels = features.pop("user_rating")
        scores = self(features)
        return self.task(
            labels=labels,
            predictions=scores,
        )
    
