using CommunityToolkit.Mvvm.Input;
using For_practice_MAUI.Models;

namespace For_practice_MAUI.PageModels
{
    public interface IProjectTaskPageModel
    {
        IAsyncRelayCommand<ProjectTask> NavigateToTaskCommand { get; }
        bool IsBusy { get; }
    }
}