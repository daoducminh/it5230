<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Menu extends Model
{
    use HasFactory;

    protected $fillable = [
        'mealtime',
        'description',
        'limit'
    ];

    protected $casts = [
        'mealtime' => 'datetime',
        'limit' => 'integer'
    ];

    public function dishes()
    {
        return $this->belongsToMany(
            'App\Models\Dish',
            'menu_details',
            'menu_id',
            'dish_id'
        );
    }
}
