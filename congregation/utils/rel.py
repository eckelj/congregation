import copy


def all_rels_have_equal_num_cols(in_rels: list):

    num_cols = len(in_rels[0].columns)
    for in_rel in in_rels:
        if len(in_rel.columns) != num_cols:
            return False

    return True


def resolve_plaintext_sets_from_rels(in_rels: list):

    if not all_rels_have_equal_num_cols(in_rels):
        raise Exception(
            f"The following input relations do not have an equal number of columns: "
            f"{[in_rel.name for in_rel in in_rels]}"
        )

    ret = []
    num_cols = len(in_rels[0].columns)

    for i in range(num_cols):
        pt_sets_for_this_col = [in_rel.columns[i].plaintext for in_rel in in_rels]
        min_pt_set = pt_sets_for_this_col[0].intersection(*pt_sets_for_this_col[1:])
        ret.append(min_pt_set)

    return ret


def resolve_trust_sets_from_rels(in_rels: list):

    if not all_rels_have_equal_num_cols(in_rels):
        raise Exception(
            f"The following input relations do not have an equal number of columns: "
            f"{[in_rel.name for in_rel in in_rels]}"
        )

    ret = []
    num_cols = len(in_rels[0].columns)

    for i in range(num_cols):
        trust_sets_for_this_col = [in_rel.columns[i].trust_with for in_rel in in_rels]
        min_trust_set = trust_sets_for_this_col[0].intersection(*trust_sets_for_this_col[1:])
        ret.append(min_trust_set)

    return ret


def get_stored_with_len(in_rel):

    sets_len = set([len(s) for s in in_rel.stored_with])
    if len(sets_len) > 1:
        raise Exception(
            f"All stored with sets should be of the same length. "
            f"Found mismatched sizes in relation {in_rel.name}"
        )
    return sets_len.pop()


def stored_with_from_rels(in_rels):

    ret = []
    for in_rel in in_rels:
        for sw in in_rel.stored_with:
            if sw not in ret:
                ret.append(copy.copy(sw))
    return ret


def non_key_cols_from_rel(output_name, start_idx: int, columns: list, key_col_idxs: list):
    """
    TODO: Might need to rethink how I propagate trust_with sets here. Main concern
     is whether some out_rel (non-key) column c should inherit it's parent trust_with
     set. The output column will be made up of all the data in the original column, but
     with removals & duplications in accordance with the output of the join. I.e. - the
     rows that remain will leak something about the key columns from the input relation.
     For now, though, it will just pass normal inheritance.
    """

    ret_cols = []
    for i, col in enumerate(columns):
        if col.idx not in set(key_col_idxs):

            indx = i + start_idx - len(key_col_idxs)
            new_col = \
                (output_name, col.name, indx, col.type_str, copy.copy(col.trust_with), copy.copy(col.plaintext))
            ret_cols.append(new_col)

    return ret_cols
