from django.urls import path,include
from . import views
urlpatterns = [
   path("",views.IndexPage,name="index"),
   path("home/",views.Index,name="home"),
   path("registration/",views.RegirtrationPage,name="registration"),
   path("login/",views.LoginPage,name="login"),
   path("registeruser/",views.RegisterUser,name="registeruser"),
   path("loginuser/",views.LoginUser,name="loginuser"),
   path("setting/<int:pk>/",views.DashboardSettingPage,name="setting"),
   path("Logout/",views.Logoutpage,name="logout"),
   path("edit/<int:pk>/",views.EditPage,name="edit"),
   path("update-data/<int:pk>/",views.UpdateData,name="update-data"),
   path("update-data-user/<int:pk>/",views.UpdateDataUser,name="update-data-user"),
   path("dashboard/",views.Dashboard,name="dashboard"),
   path("freelancelayout/",views.freelancersFullLayout,name="freelancerfulllayout"),


   
   path("settinguser/<int:pk>/",views.DashboardSettingUser,name="settinguser"),
   path("settinguseredit/<int:pk>/",views.DashboardSettingUserEdit,name="settinguseredit"),

   
   

   
   path("managecandidate/",views.DashboardCandidates,name="candidate"),
   path("managejob/",views.Dashboardjobs,name="managejob"),

   

   path("mesaages/",views.DashboardMsg,name="msg"),

   
   
   path("reviews/",views.DashboardReviews,name="reviews"),

   ###
   path("post/",views.posts,name="post"),
   path("add-post/",views.add_post,name="add-post"),
   path("view-post/",views.view_post,name="view-post"),
   path("post-detail/<int:pk>/",views.post_detail,name="post-detail"),
   path("all-post/",views.all_post_view,name="all-post"),
   path("post-edit/<int:pk>/",views.post_edit,name="post-edit"),
   path("post-delete/<int:pk>/",views.post_delete,name="post-delete"),

   path("user-post-detail/<int:pk>/",views.user_post_detail,name="user-post-detail"),
   path('wishlist/',views.wishlist,name='wishlist'),
   path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
   path('remove_from_wishlist/<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
   path('mycart/',views.mycart,name='mycart'),
   path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
   path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
   path('update-cart/<int:pk>',views.update_cart,name='update-cart'),    

   ###
   path("view_art_post/",views.view_art_post,name="view_art_post"),
   path("add_art_post/",views.add_art_post,name="add_art_post"),
   path("view_art_post_details/<int:pk>/",views.view_art_post_details,name="view_art_post_details"),
   path("view_art_post_edit/<int:pk>/",views.view_art_post_edit,name="view_art_post_edit"), 
   path("art_post_delete/<int:pk>/",views.art_post_delete,name="art_post_delete"),

   path("user_art_post_detail/<int:pk>/",views.user_art_post_detail,name="user_art_post_detail"),
   path("user_view_all_products/<int:pk>/",views.user_view_all_products,name="user_view_all_products"),
   path("user_view_all_post/<int:pk>/",views.user_view_all_post,name="user_view_all_post"),
   
   #######
   path("page404/",views.Pages404,name="page404"),
   path("checkoutpage/",views.PagesCheckout,name="checkoutpage"),
   path("contactpage/",views.PagesContact,name="contact"),
   
   path("templates/",views.PagesTemplate,name="templates"),
   
   
   path("artist_reply",views.artist_reply,name="artist_reply"),
   path("view_all_feedback/<int:pk>/",views.all_feedback,name="view_all_feedback"),
   path("feedback",views.feedback,name="feedback"),
   path("freelancer-full-profile/<int:pk>/",views.FreelancerFullProfile,name="freelancer-full-profile"),
   path("change_reviews",views.change_reviews,name="change_reviews"),
   
   path("apply-request",views.RequestPopUp, name="apply-request"),
   
   
   path("forgotpassword/", views.ForgotPassword,name="forgotpassword"),
   path("forgotpasswordpage/",views.ForgotPasswordPage,name="forgotpasswordpage"),
   path("newpassword/",views.NewPassword,name="newpassword"),
   path("change-password/",views.validateotp,name="change-password"),

   path("userallreq/",views.UserAllRequest,name="userallreq"),
   path("work-request/<int:pk>/",views.RequestStatus,name="work-request"),


    #####    Admin    ###########

   path("adminpage/",views.AdminPage,name="adminpage"),
   path("index/",views.AIndex,name="index"),
   path("inbox/",views.Inbox,name="inbox"),
   path("viewemail/",views.ViewEmail,name="viewemail"),
   path("composeemail/",views.ComposeEmail,name="composeemail"),

   path("animation/",views.Animations,name="animation"),

   path("googlemap/",views.GoogleMap,name="googlemap"),

   path("datamap/",views.DataMap,name="datamap"),

   path("codeeditor/",views.CodeEditor,name="codeeditor"),

   path("imagecropper/",views.ImageCropper,name="imagecropper"),

   path("wizard/",views.Wizard,name="wizard"),

###########    charts   #############

   path("flotchart/",views.FlotCharts,name="flotchart"),
   path("barchart/",views.BarCharts,name="barchart"),
   path("linechart/",views.LineCharts,name="linechart"),
   path("areachart/",views.AreaCharts,name="areachart"),
   
   
   
###########    Tables   #############

   path("normaltable/",views.NormalTable,name="normaltable"),
   path("datatable/",views.DataTable,name="datatable"),
   path("Editpage/<int:pk>",views.AdminEditPage,name="edittable"),
   path("update/<int:pk>",views.AdminUpdateData,name="update"),
   path("deletetabledata/<int:pk>/",views.AdminDeleteData,name="deletetabledata"),

###########    Forms   #############

   path("formelement/",views.FormElements,name="formelement"),
   path("formcomponent/",views.FormComponents,name="formcomponent"),
   path("formexample/",views.FormExamples,name="formexample"),

###############  AppViews  #############

   path("notification/",views.Notification,name="notification"),
   path("alert/",views.Alert,name="alert"),
   path("modal/",views.Modals,name="modal"),
   path("button/",views.Buttons,name="button"),
   path("tab/",views.Tabs,name="tab"),
   path("accordion/",views.Accordion,name="accordion"),
   path("dialog/",views.Dialog,name="dialog"),
   path("popover/",views.Popovers,name="popover"),
   path("tooltip/",views.ToolTips,name="tooltip"),
   path("dropdown/",views.DropDown,name="dropdown"),


###############  Pages  #############

   path("contact/",views.Contact,name="contact"),
   path("invoice/",views.Invoice,name="invoice"),
   path("typography/",views.Typography,name="typography"),
   path("color/",views.Color,name="color"),


######################################################## Paytm URLS #########################3
   path("payment/",views.initiate_payment,name="payment"),
   path("callback/",views.callback,name="callback"),

   path("add-response/<int:pk>/<slug:status>",views.add_response,name="add-response"),

]