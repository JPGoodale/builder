# local
from ivy_builder.specs.data_loader_spec import DataLoaderSpec


class JSONDataLoaderSpec(DataLoaderSpec):

    def __init__(self, dataset_spec, batch_size, window_size, num_training_sequences, num_sequences_to_use,
                 num_workers=1, unused_key_chains=None, preload_containers=False, shuffle_buffer_size=0,
                 post_proc_fn=None, prefetch_to_gpu=False, single_pass=False, float_strs=None, uint8_strs=None,
                 custom_img_strs=None, custom_img_fns=None, custom_strs=None, custom_fns=None, **kwargs):

        unused_key_chains = [] if unused_key_chains is None else unused_key_chains
        float_strs = [] if float_strs is None else float_strs
        uint8_strs = [] if uint8_strs is None else uint8_strs
        custom_img_strs = [[]] if custom_img_strs is None else custom_img_strs
        custom_img_fns = [] if custom_img_fns is None else custom_img_fns
        custom_strs = [[]] if custom_strs is None else custom_strs
        custom_fns = [] if custom_fns is None else custom_fns

        super(JSONDataLoaderSpec, self).__init__(dataset_spec,
                                                 batch_size=batch_size,
                                                 window_size=window_size,
                                                 num_training_sequences=num_training_sequences,
                                                 num_sequences_to_use=num_sequences_to_use,
                                                 num_workers=num_workers,
                                                 unused_key_chains=unused_key_chains,
                                                 preload_containers=preload_containers,
                                                 shuffle_buffer_size=shuffle_buffer_size,
                                                 post_proc_fn=post_proc_fn,
                                                 prefetch_to_gpu=prefetch_to_gpu,
                                                 single_pass=single_pass,
                                                 float_strs=float_strs,
                                                 uint8_strs=uint8_strs,
                                                 custom_img_strs=custom_img_strs,
                                                 custom_img_fns=custom_img_fns,
                                                 custom_strs=custom_strs,
                                                 custom_fns=custom_fns,
                                                 **kwargs)