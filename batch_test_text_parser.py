import json
import os
from services.processors import *
from services.notice_parser import *

BiddingNoticeProcessor = BiddingNoticeProcessor()


def single_test_file(input_file_path, output_file_path):
    input_text = ""
    with open(input_file_path, "r", encoding="utf-8") as f:
        for line in f:
            input_text += line + "\n"
    # result = BiddingNoticeProcessor.process("notice_id", input_text)
    other_service_list = ["code_extraction", "district_time",
                    "notice_type", "bid_type", "contact_info"]
    bidding_result, ori_response, cost_time = parse_bidding_product(input_text)
    winning_result, ori_response, cost_time = parse_winning_product(input_text)

    def group_res(each_curr_res, each_ori_response, each_cost_time):
        return {"result": each_curr_res, "ori_response": ori_response, "cost_time": cost_time}

    result = {"bidding_product": group_res(bidding_result, ori_response, cost_time),
              "winning_product": group_res(winning_result, ori_response, cost_time),}
    for each_service in other_service_list:
        curr_res, ori_response, cost_time = parse_other_info(input_text, each_service)
        result[each_service] = group_res(curr_res, ori_response, cost_time)

    print("input_file_path:", input_file_path)
    print("result:", result)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))


def batch_test_dir(input_dir_path, output_dir_path):
    for file in os.listdir(input_dir_path):
        input_file_path = os.path.join(input_dir_path, file)
        output_file_path = os.path.join(output_dir_path, file.replace(".txt", ".json"))
        single_test_file(input_file_path, output_file_path)


if __name__ == "__main__":
    test_input_dir = "tests/test_data/text_data_0610"
    test_output_dir = "tests/test_result/text_data_0610"
    batch_test_dir(test_input_dir, test_output_dir)

    test_input_dir = "tests/test_data/text_data_0614"
    test_output_dir = "tests/test_result/text_data_0614"
    batch_test_dir(test_input_dir, test_output_dir)



