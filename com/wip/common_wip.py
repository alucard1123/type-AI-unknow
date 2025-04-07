class CommonWip:
    def __init__(self, wip_id=None, parent_id=None, wip_type=None, content=None, raw_content=None, tag=None):
        self._wip_id = wip_id
        self._parent_id = parent_id
        self._wip_type = wip_type
        self._content = content #dict
        self._raw_content = raw_content
        # tag the domain of the wip
        self._tag = tag #list

    @property
    def content(self):
        return self._content

    @property
    def raw_content(self):
        return self._raw_content

    @property
    def wip_id(self):
        return self._wip_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def wip_type(self):
        return self._wip_type

    @property
    def tag(self):
        return self._tag

    @content.setter
    def content(self, content):
        self._content = content

    @raw_content.setter
    def raw_content(self, raw_content):
        self._raw_content = raw_content

    @wip_id.setter
    def wip_id(self, wip_id):
        self._wip_id = wip_id

    @parent_id.setter
    def parent_id(self, parent_id):
        self._parent_id = parent_id

    @wip_type.setter
    def wip_type(self, wip_type):
        self._wip_type = wip_type

    @tag.setter
    def tag(self, tag):
        self._tag = tag

