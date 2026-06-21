using For_practice_MAUI.Models;
using For_practice_MAUI.PageModels;

namespace For_practice_MAUI.Pages
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