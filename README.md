# BookEase – Serverless Hotel Booking Chatbot (AWS)

BookEase is a serverless hotel-booking chatbot built using AWS managed services. The system processes natural language input to create and manage hotel reservations, validate booking dates, calculate costs, and maintain conversational session state. The project is backend-focused and does not include a frontend interface.

---

## Project Overview

This project demonstrates the design and implementation of a cloud-native conversational system using AWS. Business logic is implemented in Python-based AWS Lambda functions, while Amazon Lex handles intent recognition and conversation orchestration. Reservation data is stored in Amazon DynamoDB.

---

## Functional Scope

- Natural language interaction through Amazon Lex
- Reservation creation and management
- Date validation logic for booking workflows
- Cost calculation based on reservation parameters
- Session management across multi-turn conversations
- Automated testing for workflow validation and edge cases
- Fully serverless backend architecture

---

## System Architecture

### AWS Services
- Amazon Lex: Intent recognition and conversational flow control
- AWS Lambda (Python): Backend logic and request processing
- Amazon DynamoDB: Persistent reservation storage
- AWS IAM: Access control and permission management

### Execution Flow
1. User input is processed by Amazon Lex
2. Lex identifies the intent and extracts slot values
3. Lex invokes AWS Lambda for fulfillment
4. Lambda validates input, calculates pricing, and manages session data
5. Reservation data is written to or read from DynamoDB
6. A response is returned to the user via Lex

---

## Data Model

**DynamoDB Table:** `Reservations`

| Attribute        | Type   | Description |
|------------------|--------|-------------|
| ReservationID   | String (PK) | Unique reservation identifier |
| GuestName       | String | Guest name |
| RoomType        | String | Room category |
| CheckInDate     | String | Start date |
| CheckOutDate    | String | End date |
| TotalCost       | Number | Calculated reservation cost |
| CreatedAt       | String | Record creation timestamp |

---

## Backend Logic

The Lambda functions are responsible for:

- Validating date ranges and booking constraints
- Calculating reservation costs based on room type and duration
- Managing conversational session state
- Handling invalid input and edge cases
- Interfacing with DynamoDB for persistence

---

## Testing

Manual tests were implemented to improve system reliability and correctness, including:

- Validation of reservation creation workflows
- Pricing calculation verification
- Date validation edge cases
- Error handling for malformed or incomplete input

These tests reduce user-facing errors and improve overall system stability.

---

## Technology Stack

- Python
- AWS Lambda
- Amazon Lex
- Amazon DynamoDB
<!-- - AWS IAM -->

---

## References

- GitHub Repository: https://github.com/Williamokogwu/BookEase  
- Amazon Lex Documentation: https://docs.aws.amazon.com/lex/  
- Amazon DynamoDB Documentation: https://docs.aws.amazon.com/dynamodb/  
- Python Documentation: https://docs.python.org/3/

---

## Author

Chijioke Okogwu  
<!-- Computer Science Major  
Graduating May 2026   -->

---

## License

This project is intended for educational and portfolio purposes.
