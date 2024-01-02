from flask import Flask, jsonify, request


@app.route('/items', methods=['POST'])
def add_item():
      # Get the item name from the request body
      item_name = request.json.get('name')

      # Add the item to the database here
      # ...

      # Delete the cached response to invalidate the cache
      cache.delete('items')

      return jsonify({'message': 'Item added successfully'})

@app.route('/items', methods=['GET'])
@cache.cached(timeout=60, key_prefix='items')
def get_items():
      # Check if the response is already cached
      cached_response = redis_client.get('items')
      if cached_response:
          return jsonify(cached_response)

      # Get the items from the database here
      items = Items.query.all()

      # Serialize the items to JSON
      serialized_items = [item.to_dict() for item in items]

      response = jsonify(serialized_items)

      return response