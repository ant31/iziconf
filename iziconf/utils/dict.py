def deep_merge(src_dict, merge_dict):
    for k, v in merge_dict.iteritems():
        if (k in src_dict and isinstance(src_dict[k], dict)):
            deep_merge(src_dict[k], merge_dict[k])
        else:
            src_dict[k] = merge_dict[k]
