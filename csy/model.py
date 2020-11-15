EMBEDDING_SIZE = 50


class RecommenderNet(keras.Model):
    def __init__(self, num_tags, num_musics, embedding_size, **kwargs):
        super(RecommenderNet, self).__init__(**kwargs)
        self.num_tags = num_tags
        self.num_musics = num_musics
        self.embedding_size = embedding_size
        self.tag_embedding = layers.Embedding(
            num_tags,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.tag_bias = layers.Embedding(num_tags, 1)
        self.music_embedding = layers.Embedding(
            num_musics,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.music_bias = layers.Embedding(num_musics, 1)

    def call(self, inputs):
        tag_vector = self.tag_embedding(inputs[:, 0])
        tag_bias = self.tag_bias(inputs[:, 0])
        music_vector = self.music_embedding(inputs[:, 1])
        music_bias = self.music_bias(inputs[:, 1])
        dot_tag_music = tf.tensordot(tag_vector, music_vector, 2)
        x = dot_tag_music + tag_bias + music_bias
        return tf.nn.sigmoid(x)


model = RecommenderNet(tag_count, music_count, EMBEDDING_SIZE)
model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(), 
    optimizer=keras.optimizers.Adam(lr=0.001)
)