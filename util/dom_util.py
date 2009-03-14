document = None

def Elem(element_name, children=[], parent_element=None, namespace=None, **attributes):
	"""Creates an element of the given name, with the given child elements.

	The keyword attributes are the attributes of the XML.
	They do not have to be strings, but can be anything that can be converted
	into a string.
	"""
	if parent_element is None:
		parent_element = document
	if namespace:
		element = parent_element.createElementNS(element_name, namespace)
	else:
		element = parent_element.createElement(element_name)
	
	for attribute_name, attribute_value in attributes.iteritems():
		if isinstance(attribute_value, bool):
			attribute_value = str(attribute_value).lower()
		elif not isinstance(attribute_value, basestring):
			attribute_value = str(attribute_value)
		element.setAttribute(attribute_name, attribute_value)

	for child in children:
		element.appendChild(child)
	return element
