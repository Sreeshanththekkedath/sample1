
from django.contrib import admin
from django.urls import path
from . import views
from . import views_2
from . import viewsRole

urlpatterns = [
    path('', views.admin,name='admin'),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    path('index', views.index,name='index'),
    path('holiday', views.holiday,name='holiday'),
    path('addholiday', views.addholiday,name='addholiday'),
    path('holiAddition', views.holiAddition,name='holiAddition'),
    path('inverts<str:pk>', views.inverts,name='inverts'),
    path('filterHoliday', views.filterHoliday,name='filterHoliday'),
    path('active', views.active,name='active'),
    path('inactive', views.inactive,name='inactive'),
    # using second view
    path('faculty', views_2.faculty,name='faculty'),
    path('addfaculty', views_2.addfaculty,name='addfaculty'),
    path('additionFaculty', views_2.additionFaculty,name='additionFaculty'),
    path('view_faculty<str:pk>', views_2.view_faculty,name='view_faculty'),
    path('EditFaculty<str:pk>', views_2.EditFaculty,name='EditFaculty'),
    path('updateFaculty<str:pk>', views_2.updateFaculty,name='updateFaculty'),
    path('addQalification<str:pk>', views_2.addQalification,name='addQalification'),
    path('QualiAddition<str:pk>', views_2.QualiAddition,name='QualiAddition'),
    path('addExperience<str:pk>', views_2.addExperience,name='addExperience'),
    path('ExpAddition<str:pk>', views_2.ExpAddition,name='ExpAddition'),
    path('deleteQua<str:pk>', views_2.deleteQua,name='deleteQua'),
    path('deleteExp<str:pk>', views_2.deleteExp,name='deleteExp'),
    path('facultyDelete<str:pk>', views_2.facultyDelete,name='facultyDelete'),
    path('delete', views_2.delete,name='delete'),
    path('deleteE', views_2.deleteE,name='deleteE'),
    path('deleteFac', views_2.deleteFac,name='deleteFac'),

    path('add_department', views_2.add_department,name='add_department'),
    path('Department', views_2.Department,name='Department'),
    path('depAddition', views_2.depAddition,name='depAddition'),
    path('filterdepartment', views_2.filterdepartment,name='filterdepartment'),
    path('view_dep<str:pk>', views_2.view_dep,name='view_dep'),
    path('edit_dep<str:pk>', views_2.edit_dep,name='edit_dep'),
    path('UpdateDepartment', views_2.UpdateDepartment,name='UpdateDepartment'),
    path('depinverts<str:pk>', views_2.depinverts,name='depinverts'),

    path('active_dep', views_2.active_dep,name='active_dep'),
    path('inactive_dep', views_2.inactive_dep,name='inactive_dep'),   
    path('filterfaculty', views_2.filterfaculty,name='filterfaculty'),

    # create a seperate view for role
    path('role', viewsRole.role,name='role'),
    path('addRole', viewsRole.addRole,name='addRole'),
    path('roleAddition', viewsRole.roleAddition,name='roleAddition'),
    path('actInact<str:pk>', viewsRole.actInact,name='actInact'),
    path('roleactive', viewsRole.roleactive,name='roleactive'),
    path('roleinactive', viewsRole.roleinactive,name='roleinactive'),
    path('editRole<str:pk>', viewsRole.editRole,name='editRole'),
    path('roleEdit', viewsRole.roleEdit,name='roleEdit'),
    path('path', viewsRole.path,name='path'),
    path('addPath', viewsRole.addPath,name='addPath'),
    path('pathAddition', viewsRole.pathAddition,name='pathAddition'),
    path('editPath<str:pk>', viewsRole.editPath,name='editPath'),
    path('PathEdit', viewsRole.PathEdit,name='PathEdit'),
    path('permisson<str:pk>', viewsRole.permisson,name='permisson'),
    path('savePermission', viewsRole.savePermission,name='savePermission'),
    path('deletePath<str:pk>', viewsRole.deletePath,name='deletePath'),
    path('user', viewsRole.user,name='user'),
    path('addUser', viewsRole.addUser,name='addUser'),
    path('userAddition', viewsRole.userAddition,name='userAddition'),
    path('userFilter', viewsRole.userFilter,name='userFilter'),
    path('viewUser<str:pk>', viewsRole.viewUser,name='viewUser'),
    path('ChangePSWD', viewsRole.ChangePSWD,name='ChangePSWD'),
    path('EditUser<str:pk>', viewsRole.EditUser,name='EditUser'),
    path('UpdateUser', viewsRole.UpdateUser,name='UpdateUser'),
    path('statuser<str:pk>', viewsRole.statuser,name='statuser'),
    path('inactivateUser', viewsRole.inactivateUser,name='inactivateUser'),
    path('activateUser', viewsRole.activateUser,name='activateUser'),

]

