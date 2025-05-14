from dataclasses import dataclass, asdict
from typing import List, Optional
import json
from dataclasses import field
import os

@dataclass
class Test:
    q: str
    a: str

@dataclass
class TestData:
    question: str
    answer: int
    test: Optional[Test] = None

    def to_dict(self):
        """Convert TestData to dictionary, excluding None values"""
        result = {
            'question': self.question,
            'answer': self.answer
        }
        if self.test is not None:
            result['test'] = asdict(self.test)
        return result

@dataclass
class TaskJson:
    apikey: str
    description: str
    copyright: str
    test_data: List[TestData]

def read_task_json(file_path: str) -> TaskJson:
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    # Convert the raw JSON data into our data classes
    test_data_list = []
    for item in data['test-data']:
        test = None
        if 'test' in item:
            test = Test(**item['test'])
        
        test_data = TestData(
            question=item['question'],
            answer=item['answer'],
            test=test
        )
        test_data_list.append(test_data)
    
    return TaskJson(
        apikey=data['apikey'],
        description=data['description'],
        copyright=data['copyright'],
        test_data=test_data_list
    )

def process_test_data(task_json: TaskJson) -> TaskJson:
    """
    Process the test data and create a new TaskJson object.
    You can modify this function to implement your specific processing logic.
    """
    # Example processing: Add 1000 to each answer
    for item in task_json.test_data:
        item.answer += 1000
    
    return task_json

def save_task_json(task_json: TaskJson, output_file: str):
    # Create a custom dictionary that excludes None values
    data = {
        'apikey': task_json.apikey,
        'description': task_json.description,
        'copyright': task_json.copyright,
        'test-data': [item.to_dict() for item in task_json.test_data]
    }
    
    # Save to file with pretty printing
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create paths relative to the script location
    input_file = os.path.join(script_dir, "task.json")
    output_file = os.path.join(script_dir, "processed_task.json")
    
    # Read the original JSON file
    task_json = read_task_json(input_file)
    
    # Process the data
    processed_task_json = process_test_data(task_json)
    
    # Save to a new file
    save_task_json(processed_task_json, output_file)
    
    print(f"Processing complete. Output saved to {output_file}")

if __name__ == "__main__":
    main() 