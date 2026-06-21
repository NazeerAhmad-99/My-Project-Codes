using MAUI_first_project.Models;
using MAUI_first_project.PageModels;

namespace MAUI_first_project.Pages
{
    public partial class MainPage : ContentPage
    {
        public MainPage(MainPageModel model)
        {
            InitializeComponent();
            BindingContext = model;
        }
    }
}