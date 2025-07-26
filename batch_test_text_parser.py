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
    bidding_result = parse_bidding_product(input_text)
    winning_result = parse_winning_product(input_text)
    result = {"bidding_product": bidding_result, "winning_product": winning_result}

    print("input_file_path:", input_file_path)
    print("result:", result)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))


def batch_test_dir(input_dir_path, output_dir_path):
    for file in os.listdir(input_dir_path):
        input_file_path = os.path.join(input_dir_path, file)
        output_file_path = os.path.join(output_dir_path, file)
        single_test_file(input_file_path, output_file_path)


if __name__ == "__main__":
    test_input_dir = "tests/test_data/text_data_0610"
    test_output_dir = "tests/test_result/text_data_0610"
    batch_test_dir(test_input_dir, test_output_dir)



