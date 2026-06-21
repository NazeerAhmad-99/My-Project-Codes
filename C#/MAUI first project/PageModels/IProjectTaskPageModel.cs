using CommunityToolkit.Mvvm.Input;
using MAUI_first_project.Models;

namespace MAUI_first_project.PageModels
{
    public interface IProjectTaskPageModel
    {
        IAsyncRelayCommand<ProjectTask> NavigateToTaskCommand { get; }
        bool IsBusy { get; }
    }
}