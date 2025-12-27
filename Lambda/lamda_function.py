import json
import random
import string
import boto3
from datetime import datetime

# Initialize DynamoDB table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BookEaseReservations')

# Helper: Generate a random reservation ID
def generate_reservation_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Main Lambda handler
def lambda_handler(event, context):
    print("🔷 Incoming event:")
    print(json.dumps(event, indent=2))

    try:
        intent_name = event['sessionState']['intent']['name']
        slots = event['sessionState']['intent'].get('slots', {})

        # GREETING INTENT
        if intent_name == 'GreetingIntent':
            message = {
                "contentType": "PlainText",
                "content": "Thank you for contacting BookEase. What would you like to do today? 1. Book a room 2. Check your reservation"
            }
            return {
                "sessionState": {
                    "dialogAction": {"type": "ElicitIntent"},
                    "sessionAttributes": event['sessionState'].get('sessionAttributes', {})
                },
                "messages": [message]
            }

        # BOOKROOM INTENT
        elif intent_name == 'BookRoomIntent':
            confirmation = slots.get('confirmBooking', {}).get('value', {}).get('interpretedValue', '').lower()

            if confirmation in ['yes', 'true', 'y']:
                # Extract all required slot values safely
                try:
                    reservation_id = generate_reservation_id()
                    item = {
                        'reservationId': reservation_id,
                        'firstName': slots['firstName']['value']['interpretedValue'],
                        'lastName': slots['lastname']['value']['interpretedValue'],
                        'phoneNumber': slots['phoneNumber']['value']['interpretedValue'],
                        'emailAddress': slots['emailAddress']['value']['interpretedValue'],
                        'checkInDate': slots['checkInDate']['value']['interpretedValue'],
                        'checkOutDate': slots['checkoutDate']['value']['interpretedValue'],
                        'roomType': slots['roomType']['value']['interpretedValue'],
                        'createdAt': datetime.now().isoformat()
                    }

                    # Save to DynamoDB
                    table.put_item(Item=item)
                    print("✅ Reservation saved:", json.dumps(item, indent=2))

                    message = {
                        "contentType": "PlainText",
                        "content": f"✅ Booking confirmed!\nReservation ID: {reservation_id}\nThank you for choosing BookEase!"
                    }
                    return close(event, message)

                except Exception as slot_error:
                    print("❌ Error extracting slot values:", str(slot_error))
                    return close(event, {
                        "contentType": "PlainText",
                        "content": "⚠️ Error saving your booking. Please try again later."
                    })

            elif confirmation in ['no', 'false', 'n']:
                message = {
                    "contentType": "PlainText",
                    "content": "❌ Booking cancelled.\nWould you like to 1. Book a room or 2. Check your reservation?"
                }
                return close(event, message)

            else:
                message = {
                    "contentType": "PlainText",
                    "content": "Please confirm your booking by responding Yes or No."
                }
                return elicit_slot(event, 'confirmBooking', message)

        # CHECK RESERVATION INTENT
        elif intent_name == 'CheckReservationIntent':
            reservation_id = slots.get('reservationId', {}).get('value', {}).get('interpretedValue')
            


            # if not reservation_id:
            #     return elicit_slot(event, 'reservationId', {
            #         "contentType": "PlainText",
            #         "content": "Please provide your reservation ID."
            #     })

            if not reservation_id:
                return elicit_slot(event, 'reservationId', {
                    "contentType": "PlainText",
                    "content": "Please provide your reservation ID."
                })

            # Normalize case to match how it was saved
            reservation_id = reservation_id.upper()

            print("🔍 Searching for reservationId:", reservation_id)

            try:
                response = table.get_item(Key={'reservationId': reservation_id})
                if 'Item' in response:
                    item = response['Item']
                    content = (
                        f"📄 Reservation Details:\n"
                        f"Name: {item['firstName']} {item['lastName']}\n"
                        f"Room: {item['roomType']}\n"
                        f"Check-in: {item['checkInDate']}\n"
                        f"Check-out: {item['checkOutDate']}\n"
                        f"Email: {item['emailAddress']}\n"
                        f"Phone: {item['phoneNumber']}"
                    )
                else:
                    content = "⚠️ No reservation found with that ID."

                return close(event, {"contentType": "PlainText", "content": content})

            except Exception as e:
                print("❌ Error fetching reservation:", str(e))
                return close(event, {
                    "contentType": "PlainText",
                    "content": "⚠️ Could not retrieve your reservation. Try again later."
                })

        # FALLBACK INTENT
        elif intent_name == 'FallbackIntent':
            return close(event, {
                "contentType": "PlainText",
                "content": "❓ I'm not sure I understood that. Please type 'Book a room' or 'Check my reservation'."
            })

        # UNKNOWN INTENT
        else:
            return close(event, {
                "contentType": "PlainText",
                "content": "🤖 Sorry, I didn't recognize that request."
            })

    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return close(event, {
            "contentType": "PlainText",
            "content": "⚠️ Oops! Something went wrong. Please try again."
        })

# Close the conversation
def close(event, message):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "state": "Fulfilled",
                "slots": event['sessionState']['intent'].get('slots', {})
            },
            "sessionAttributes": event['sessionState'].get('sessionAttributes', {}),
            "originatingRequestId": event['sessionState'].get('originatingRequestId')
        },
        "messages": [message]
    }

# Request for missing slot
def elicit_slot(event, slot_to_elicit, message):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": slot_to_elicit
            },
            "intent": event['sessionState']['intent'],
            "sessionAttributes": event['sessionState'].get('sessionAttributes', {})
        },
        "messages": [message]
    }
