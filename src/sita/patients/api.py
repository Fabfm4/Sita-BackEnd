from sita.core.api.viewsets import GenericViewSet
from sita.api.v1.routers import router
from sita.core.api.viewsets.nested import NestedViewset
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientSerializer
from sita.users.api import UserViewSet

class PatientViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PatientSerializer

    def list(self, request, *args, **kwards):
        """
        Create user by Admin.
        ---
        view_mocker: 'Patient'
        omit_serializer: true
        omit_parameters:
            - form
        parameters:
            - name: body
              type: UserSerializer
              paramType: body
              description:
                'email: <b>required</b> <br>
                password: <b>required</b> <br>
                name:NOT required <br>
                firstName: NOT required <br>
                mothersName: NOT required <br>
                phone: NOT required'
            - name: Authorization
              description: Bearer {token}.
              required: true
              type: string
              paramType: header
        responseMessages:
            - code: 201
              message: CREATED
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR
        consumes:
            - application/json
        produces:
            - application/json
        """
        pass

    def my_view_mocker(view):
        view.request.tacos = 'tasty'
        return view


router.register_nested(
    r'user',
    r'patient',
    PatientViewSet,
    parent_lookup_name='user',
    base_name='patient'
)
