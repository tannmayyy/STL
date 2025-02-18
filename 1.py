import streamlit as st
from streamlit_condition_tree import condition_tree

config = {
  'fields': {
      'firstName': {
        'label': 'First name',
        'type': 'text',
        'operators': ['equal', 'not_equal', 'in', 'not_in'],
        'mainWidgetProps': {
          'valuePlaceholder': 'Enter name(s) separated by commas',
        },
      },
      'age': {
        'label': 'Age',
        'type': 'number',
        'fieldSettings': {
          'min': 0,
          'max': 140
        },
        'preferWidgets': ['slider', 'rangeslider'],
      },
      'color': {
        'label': 'Favorite color',
        'type': 'select',
        'operators': ['equal', 'not_equal', 'in', 'not_in'],
        'fieldSettings': {
          'listValues': [
              {'value': 'yellow', 'title': 'Yellow'},
              {'value': 'green', 'title': 'Green'},
              {'value': 'orange', 'title': 'Orange'},
          ],
        },
        'mainWidgetProps': {
          'customInput': True,  # Enables custom values in addition to predefined ones
          'valuePlaceholder': 'Select or enter multiple colors',
        },
      },
      'like_tomatoes': {
        'label': 'Likes tomatoes',
        'type': 'boolean',
        'operators': ['equal'],
      },
      'birth_date': {
        'label': 'Date of birth',
        'type': 'date',
        'operators': ['less', 'equal']
      }
  },
}

query_string = condition_tree(
  config,
  return_type='sql',
  placeholder='Build your query'
)

st.write("Generated SQL Query:")
st.code(query_string)
