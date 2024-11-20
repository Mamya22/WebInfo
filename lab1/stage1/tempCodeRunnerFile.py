    ret = []
        L1_id_list = T1[0]
        L2_id_list = T2[0]
        L1_skip_list = T1[1]
        L2_skip_list = T2[1]
        
        if not L1_id_list or not L2_id_list:
            status_window.update_status(Fore.RED + "The operand 'NOT' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            
            while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                # try_skip for index1
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:
                    if (index1 // interval_1 in L1_skip_list and
                        L1_id_list[index1] == L2_id_list[index2] and
                        L1_id_list[L1_skip_list[index1 // interval_1][1]] == L2_id_list[index2]):
                        
                        index1 += interval_1
                        index2 += 1
                    elif (index1 // interval_1 in L1_skip_list and
                        L1_id_list[index1] < L2_id_list[index2] and
                        L1_id_list[L1_skip_list[index1 // interval_1][1]] < L2_id_list[index2]):
                        
                        index1 += interval_1
                    else:
                        break

                # try_skip for index2
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:
                    if (index2 // interval_2 in L2_skip_list and
                        L2_id_list[index2] == L1_id_list[index1] and
                        L2_id_list[L2_skip_list[index2 // interval_2][1]] == L1_id_list[index1]):
                        
                        index2 += interval_2
                        index1 += 1
                    elif (index2 // interval_2 in L2_skip_list and
                        L2_id_list[index2] < L1_id_list[index1] and
                        L2_id_list[L2_skip_list[index2 // interval_2][1]] < L1_id_list[index1]):
                        
                        index2 += interval_2
                    else:
                        break

                # Compare elements at index1 and index2
                if index1 < len_1 and index2 < len_2:
                    try:
                        val1 = int(L1_id_list[index1])
                        val2 = int(L2_id_list[index2])
                    except ValueError:
                        print(f"Skipping invalid comparison: {L1_id_list[index1]}, {L2_id_list[index2]}")
                        if isinstance(L1_id_list[index1], str):
                            index1 += 1
                        if isinstance(L2_id_list[index2], str):
                            index2 += 1
                        continue

                    if val1 == val2:
                        index1 += 1
                        index2 += 1
                    elif val1 < val2:
                        ret.append(val1)
                        index1 += 1
                    else:
                        index2 += 1

            # Append remaining elements from L1_id_list
            if index1 < len(L1_id_list):
                ret.extend(L1_id_list[index1:])

        return ret, self